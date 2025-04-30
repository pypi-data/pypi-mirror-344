from __future__ import annotations

import dataclasses
from collections import deque
from collections.abc import Callable, Generator, Mapping
from contextlib import contextmanager
from typing import Any, ClassVar

import torchmetrics
from lightning.pytorch import LightningModule
from lightning.pytorch.utilities.types import _METRIC
from lightning_utilities.core.rank_zero import rank_zero_warn
from typing_extensions import override

from ...util.typing_utils import mixin_base_type


@dataclasses.dataclass(frozen=True, kw_only=True)
class _LogContextKwargs:
    __ignore_fields__: ClassVar[set[str]] = {"prefix", "disabled"}

    prefix: str | None = None
    disabled: bool | None = None
    prog_bar: bool | None = None
    logger: bool | None = None
    on_step: bool | None = None
    on_epoch: bool | None = None
    reduce_fx: str | Callable | None = None
    enable_graph: bool | None = None
    sync_dist: bool | None = None
    sync_dist_group: Any | None = None
    add_dataloader_idx: bool | None = None
    batch_size: int | None = None
    rank_zero_only: bool | None = None

    def to_dict(self):
        d = dataclasses.asdict(self)
        for field in self.__ignore_fields__:
            d.pop(field, None)

        # Pop all None values
        for k in list(d.keys()):
            if d[k] is None:
                d.pop(k)

        return d


class LoggerLightningModuleMixin(mixin_base_type(LightningModule)):
    @override
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._logger_prefix_stack = deque[_LogContextKwargs]()

    @property
    def logging_enabled(self) -> bool:
        # Logging is disabled in barebones mode.
        if (trainer := self._trainer) is not None and trainer.barebones:
            # Warn the user once that logging is disabled in barebones mode.
            if not hasattr(self, "_barebones_logging_warned"):
                rank_zero_warn(
                    "Logging is disabled in barebones mode. "
                    "This is to reduce the overhead of logging in barebones mode. "
                    "If you want to enable logging, set `barebones=False` in the Trainer.",
                )
                self._barebones_logging_warned = True
            return False

        # If no loggers are registered, then logging is disabled.
        if not self.logger:
            return False

        # Check if the topmost non-null context is disabled
        for context in reversed(self._logger_prefix_stack):
            if context.disabled is not None:
                return not context.disabled

        # Otherwise, logging is enabled.
        return True

    @contextmanager
    def log_context(
        self,
        prefix: str | None = None,
        disabled: bool | None = None,
        prog_bar: bool | None = None,
        logger: bool | None = None,
        on_step: bool | None = None,
        on_epoch: bool | None = None,
        reduce_fx: str | Callable | None = None,
        enable_graph: bool | None = None,
        sync_dist: bool | None = None,
        sync_dist_group: Any | None = None,
        add_dataloader_idx: bool | None = None,
        batch_size: int | None = None,
        rank_zero_only: bool | None = None,
    ) -> Generator[None, None, None]:
        self._logger_prefix_stack.append(
            _LogContextKwargs(
                prefix=prefix,
                disabled=disabled,
                prog_bar=prog_bar,
                logger=logger,
                on_step=on_step,
                on_epoch=on_epoch,
                reduce_fx=reduce_fx,
                enable_graph=enable_graph,
                sync_dist=sync_dist,
                sync_dist_group=sync_dist_group,
                add_dataloader_idx=add_dataloader_idx,
                batch_size=batch_size,
                rank_zero_only=rank_zero_only,
            )
        )
        try:
            yield
        finally:
            _ = self._logger_prefix_stack.pop()

    def _make_prefix_and_kwargs_dict(self, kwargs: _LogContextKwargs):
        prefix = "".join(c.prefix for c in self._logger_prefix_stack if c.prefix)

        fn_kwargs: dict[str, Any] = {}
        for c in self._logger_prefix_stack:
            fn_kwargs.update(c.to_dict())

        fn_kwargs.update(kwargs.to_dict())
        return prefix, fn_kwargs

    @override
    def log(
        self,
        name: str,
        value: _METRIC,
        prog_bar: bool | None = None,
        logger: bool | None = None,
        on_step: bool | None = None,
        on_epoch: bool | None = None,
        reduce_fx: str | Callable | None = None,
        enable_graph: bool | None = None,
        sync_dist: bool | None = None,
        sync_dist_group: Any | None = None,
        add_dataloader_idx: bool | None = None,
        batch_size: int | None = None,
        metric_attribute: str | None = None,
        rank_zero_only: bool | None = None,
    ) -> None:
        """Log a key, value pair.

        Example::

            self.log('train_loss', loss)

        The default behavior per hook is documented here: :ref:`extensions/logging:Automatic Logging`.

        Args:
            name: key to log. Must be identical across all processes if using DDP or any other distributed strategy.
            value: value to log. Can be a ``float``, ``Tensor``, or a ``Metric``.
            prog_bar: if ``True`` logs to the progress bar.
            logger: if ``True`` logs to the logger.
            on_step: if ``True`` logs at this step. The default value is determined by the hook.
                See :ref:`extensions/logging:Automatic Logging` for details.
            on_epoch: if ``True`` logs epoch accumulated metrics. The default value is determined by the hook.
                See :ref:`extensions/logging:Automatic Logging` for details.
            reduce_fx: reduction function over step values for end of epoch. :meth:`torch.mean` by default.
            enable_graph: if ``True``, will not auto detach the graph.
            sync_dist: if ``True``, reduces the metric across devices. Use with care as this may lead to a significant
                communication overhead.
            sync_dist_group: the DDP group to sync across.
            add_dataloader_idx: if ``True``, appends the index of the current dataloader to
                the name (when using multiple dataloaders). If False, user needs to give unique names for
                each dataloader to not mix the values.
            batch_size: Current batch_size. This will be directly inferred from the loaded batch,
                but for some data structures you might need to explicitly provide it.
            metric_attribute: To restore the metric state, Lightning requires the reference of the
                :class:`torchmetrics.Metric` in your model. This is found automatically if it is a model attribute.
            rank_zero_only: Tells Lightning if you are calling ``self.log`` from every process (default) or only from
                rank 0. If ``True``, you won't be able to use this metric as a monitor in callbacks
                (e.g., early stopping). Warning: Improper use can lead to deadlocks! See
                :ref:`Advanced Logging <visualize/logging_advanced:rank_zero_only>` for more details.

        """
        # If logging is disabled, then do nothing.
        if not self.logging_enabled:
            return

        prefix, fn_kwargs = self._make_prefix_and_kwargs_dict(
            _LogContextKwargs(
                prog_bar=prog_bar,
                logger=logger,
                on_step=on_step,
                on_epoch=on_epoch,
                reduce_fx=reduce_fx,
                enable_graph=enable_graph,
                sync_dist=sync_dist,
                sync_dist_group=sync_dist_group,
                add_dataloader_idx=add_dataloader_idx,
                batch_size=batch_size,
                rank_zero_only=rank_zero_only,
            )
        )
        name = f"{prefix}{name}"
        return super().log(name, value, metric_attribute=metric_attribute, **fn_kwargs)

    def log_dict(
        self,
        dictionary: Mapping[str, _METRIC] | torchmetrics.MetricCollection,
        prog_bar: bool | None = None,
        logger: bool | None = None,
        on_step: bool | None = None,
        on_epoch: bool | None = None,
        reduce_fx: str | Callable | None = None,
        enable_graph: bool | None = None,
        sync_dist: bool | None = None,
        sync_dist_group: Any | None = None,
        add_dataloader_idx: bool | None = None,
        batch_size: int | None = None,
        rank_zero_only: bool | None = None,
    ) -> None:
        """Log a dictionary of values at once.

        Example::

            values = {'loss': loss, 'acc': acc, ..., 'metric_n': metric_n}
            self.log_dict(values)

        Args:
            dictionary: key value pairs.
                Keys must be identical across all processes if using DDP or any other distributed strategy.
                The values can be a ``float``, ``Tensor``, ``Metric``, or ``MetricCollection``.
            prog_bar: if ``True`` logs to the progress base.
            logger: if ``True`` logs to the logger.
            on_step: if ``True`` logs at this step.
                ``None`` auto-logs for training_step but not validation/test_step.
                The default value is determined by the hook.
                See :ref:`extensions/logging:Automatic Logging` for details.
            on_epoch: if ``True`` logs epoch accumulated metrics.
                ``None`` auto-logs for val/test step but not ``training_step``.
                The default value is determined by the hook.
                See :ref:`extensions/logging:Automatic Logging` for details.
            reduce_fx: reduction function over step values for end of epoch. :meth:`torch.mean` by default.
            enable_graph: if ``True``, will not auto-detach the graph
            sync_dist: if ``True``, reduces the metric across GPUs/TPUs. Use with care as this may lead to a significant
                communication overhead.
            sync_dist_group: the ddp group to sync across.
            add_dataloader_idx: if ``True``, appends the index of the current dataloader to
                the name (when using multiple). If ``False``, user needs to give unique names for
                each dataloader to not mix values.
            batch_size: Current batch size. This will be directly inferred from the loaded batch,
                but some data structures might need to explicitly provide it.
            rank_zero_only: Tells Lightning if you are calling ``self.log`` from every process (default) or only from
                rank 0. If ``True``, you won't be able to use this metric as a monitor in callbacks
                (e.g., early stopping). Warning: Improper use can lead to deadlocks! See
                :ref:`Advanced Logging <visualize/logging_advanced:rank_zero_only>` for more details.

        """

        _, fn_kwargs = self._make_prefix_and_kwargs_dict(
            _LogContextKwargs(
                prog_bar=prog_bar,
                logger=logger,
                on_step=on_step,
                on_epoch=on_epoch,
                reduce_fx=reduce_fx,
                enable_graph=enable_graph,
                sync_dist=sync_dist,
                sync_dist_group=sync_dist_group,
                add_dataloader_idx=add_dataloader_idx,
                batch_size=batch_size,
                rank_zero_only=rank_zero_only,
            )
        )
        # NOTE: Prefix will be handled by the individual log calls.
        return super().log_dict(dictionary, **fn_kwargs)
