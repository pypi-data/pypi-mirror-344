from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any, Generic, Literal, TypedDict, cast

import nshconfig as C
import torch
import torch.distributed
from lightning.pytorch import LightningModule
from lightning.pytorch.profilers import PassThroughProfiler, Profiler
from lightning.pytorch.utilities.model_helpers import is_overridden
from lightning.pytorch.utilities.rank_zero import rank_zero_warn
from typing_extensions import Never, TypeVar, deprecated, override

from ..callbacks.rlp_sanity_checks import RLPSanityCheckModuleMixin
from .mixins.callback import CallbackModuleMixin
from .mixins.debug import DebugModuleMixin
from .mixins.logger import LoggerLightningModuleMixin

log = logging.getLogger(__name__)

THparams = TypeVar("THparams", bound=C.Config, infer_variance=True)


T = TypeVar("T", infer_variance=True)

ReduceOpStr = Literal[
    "avg",
    "mean",
    "band",
    "bor",
    "bxor",
    "max",
    "min",
    "premul_sum",
    "product",
    "sum",
]
VALID_REDUCE_OPS = (
    "avg",
    "mean",
    "band",
    "bor",
    "bxor",
    "max",
    "min",
    "premul_sum",
    "product",
    "sum",
)


class IndividualSample(TypedDict):
    """
    A dictionary that contains the individual sample.
    This is used to split the batched predictions into individual predictions.
    """

    index: int
    """The index of the sample in the batch."""

    batch: Any
    """The batch to split."""

    prediction: Any
    """The batched prediction to split."""


def default_split_batched_predictions(
    batch: Any,
    prediction: Any,
    batch_indices: Sequence[Any],
) -> Iterable[IndividualSample]:
    """
    Splits the batched predictions into a list of individual predictions.
    Args:
        batch: The batch to split.
        prediction: The batched prediction to split.
        batch_indices: The indices of the batches.
    Returns:
        A tuple of two sequences: the corresponding batches and the individual predictions.
    """
    import torch.utils._pytree as tree

    for i, global_idx in enumerate(batch_indices):

        def _verify_and_index(x: torch.Tensor):
            # Make sure dim 0 length is equal to the batch size,
            # otherwise we can't index it and should prompt
            # the user to implement a splitter
            if x.shape[0] != len(batch_indices):
                raise ValueError(
                    f"Batch size {x.shape[0]} does not match the number of batch indices {len(batch_indices)}. "
                    "Please implement a custom `split_batched_predictions` method in your LightningModuleBase class."
                )

            return x[i]

        # Create a dictionary for each sample
        yield IndividualSample(
            index=global_idx,
            batch=tree.tree_map(_verify_and_index, batch),
            prediction=tree.tree_map(_verify_and_index, prediction),
        )


class LightningModuleBase(
    DebugModuleMixin,
    RLPSanityCheckModuleMixin,
    LoggerLightningModuleMixin,
    CallbackModuleMixin,
    LightningModule,
    ABC,
    Generic[THparams],
):
    # region Profiler
    @property
    def profiler(self) -> Profiler:
        if (trainer := self._trainer) is None:
            raise RuntimeError("trainer is not defined")

        if not hasattr(trainer, "profiler"):
            raise RuntimeError("trainer does not have profiler")

        if (profiler := getattr(trainer, "profiler")) is None:
            profiler = PassThroughProfiler()

        return profiler

    # endregion

    # region Distributed
    def all_gather_object(
        self,
        object: T,
        group: torch.distributed.ProcessGroup | None = None,
    ) -> list[T]:
        if (
            not torch.distributed.is_available()
            or not torch.distributed.is_initialized()
        ):
            return [object]

        object_list = [cast(T, None) for _ in range(self.trainer.world_size)]
        torch.distributed.all_gather_object(object_list, object, group=group)
        return object_list

    def barrier(self, name: str | None = None):
        return self.trainer.strategy.barrier(name=name)

    def reduce(
        self,
        tensor: torch.Tensor,
        reduce_op: torch.distributed.ReduceOp.RedOpType | ReduceOpStr,
        group: Any | None = None,
    ) -> torch.Tensor:
        if isinstance(reduce_op, str):
            # validate reduce_op
            if reduce_op not in VALID_REDUCE_OPS:
                raise ValueError(
                    f"reduce_op must be one of {VALID_REDUCE_OPS}, got {reduce_op}"
                )

        return self.trainer.strategy.reduce(tensor, group=group, reduce_op=reduce_op)

    # endregion

    # Our own custom __repr__ method.
    # Torch's __repr__ method is too verbose and doesn't provide any useful information.
    @override
    def __repr__(self):
        parts: list[str] = []
        parts.append(f"hparams={repr(self.hparams)}")
        parts.append(f"device={self.device}")
        if self.debug:
            parts.append("debug=True")

        parts_str = ", ".join(parts)
        return f"{self.__class__.__name__}({parts_str})"

    @property
    @override
    def hparams(self) -> THparams:  # pyright: ignore[reportIncompatibleMethodOverride]
        return cast(THparams, super().hparams)

    @property
    @override
    def hparams_initial(self) -> THparams:  # pyright: ignore[reportIncompatibleMethodOverride]
        hparams = cast(THparams, super().hparams_initial)
        return hparams

    @property
    @deprecated("Use `hparams` instead")
    def config(self):
        return cast(Never, self.hparams)

    @classmethod
    @abstractmethod
    def hparams_cls(cls) -> type[THparams]: ...

    @override
    def __init__(self, hparams: THparams | Mapping[str, Any]):
        super().__init__()

        # Validate and save hyperparameters
        hparams_cls = self.hparams_cls()
        if isinstance(hparams, Mapping):
            hparams = hparams_cls.model_validate(hparams)
        elif not isinstance(hparams, hparams_cls):
            raise TypeError(
                f"Expected hparams to be either a Mapping or an instance of {hparams_cls}, got {type(hparams)}"
            )
        hparams = hparams.model_deep_validate()
        self.save_hyperparameters(hparams)

    def zero_loss(self):
        """
        Returns a loss tensor with the value 0.
        It multiples each weight by 0 and returns the sum, so we don't run into issues with ununsed parameters in DDP.
        """
        loss = sum((0.0 * v).sum() for v in self.parameters() if v.requires_grad)
        loss = cast(torch.Tensor, loss)
        return loss

    def split_batched_predictions(
        self,
        batch: Any,
        prediction: Any,
        batch_indices: Sequence[Any],
    ) -> Iterable[IndividualSample]:
        """
        Splits the batched predictions into a list of individual predictions.
        Args:
            batch: The batch to split.
            prediction: The batched prediction to split.
            batch_indices: The indices of the batches.
        Returns:
            A tuple of two sequences: the corresponding batches and the individual predictions.
        """
        return default_split_batched_predictions(batch, prediction, batch_indices)

    @override
    @classmethod
    def load_from_checkpoint(cls, *args, **kwargs) -> Never:
        raise ValueError("This method is not supported. Use `from_checkpoint` instead.")

    @classmethod
    def hparams_from_checkpoint(
        cls,
        ckpt_or_path: dict[str, Any] | str | Path,
        /,
        strict: bool | None = None,
        *,
        update_hparams: Callable[[THparams], THparams] | None = None,
        update_hparams_dict: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
    ):
        if isinstance(ckpt_or_path, dict):
            ckpt = ckpt_or_path
        else:
            ckpt = torch.load(ckpt_or_path, map_location="cpu")

        if (hparams := ckpt.get(cls.CHECKPOINT_HYPER_PARAMS_KEY)) is None:
            raise ValueError(
                f"The checkpoint does not contain hyperparameters. It must contain the key '{cls.CHECKPOINT_HYPER_PARAMS_KEY}'."
            )
        if update_hparams_dict is not None:
            hparams = update_hparams_dict(hparams)

        hparams = cls.hparams_cls().model_validate(hparams, strict=strict)
        if update_hparams is not None:
            hparams = update_hparams(hparams)

        return hparams

    @classmethod
    def from_checkpoint(
        cls,
        ckpt_or_path: dict[str, Any] | str | Path,
        /,
        strict: bool | None = None,
        map_location: torch.serialization.MAP_LOCATION = None,
        *,
        update_hparams: Callable[[THparams], THparams] | None = None,
        update_hparams_dict: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
    ):
        # Load checkpoint
        if isinstance(ckpt_or_path, Mapping):
            ckpt = ckpt_or_path
        else:
            ckpt = torch.load(ckpt_or_path, map_location=map_location)

        # Load hyperparameters from checkpoint
        hparams = cls.hparams_from_checkpoint(
            ckpt,
            strict=strict,
            update_hparams=update_hparams,
            update_hparams_dict=update_hparams_dict,
        )

        # Load model from checkpoint
        model = cls(hparams)

        # Load model state from checkpoint
        if (
            model._strict_loading is not None
            and strict is not None
            and strict != model.strict_loading
        ):
            raise ValueError(
                f"You set `.load_from_checkpoint(..., strict={strict!r})` which is in conflict with"
                f" `{cls.__name__}.strict_loading={model.strict_loading!r}. Please set the same value for both of them."
            )
        strict = model.strict_loading if strict is None else strict

        if is_overridden("configure_model", model):
            model.configure_model()

        # give model a chance to load something
        model.on_load_checkpoint(ckpt)

        # load the state_dict on the model automatically

        keys = model.load_state_dict(ckpt["state_dict"], strict=strict)

        if not strict:
            if keys.missing_keys:
                rank_zero_warn(
                    f"Found keys that are in the model state dict but not in the checkpoint: {keys.missing_keys}"
                )
            if keys.unexpected_keys:
                rank_zero_warn(
                    f"Found keys that are not in the model state dict but in the checkpoint: {keys.unexpected_keys}"
                )

        return model
