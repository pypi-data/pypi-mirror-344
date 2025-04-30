from __future__ import annotations

import math
from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Literal

import nshconfig as C
from lightning.pytorch import LightningModule
from lightning.pytorch.utilities.types import (
    LRSchedulerConfigType,
    LRSchedulerTypeUnion,
)
from torch.optim import Optimizer
from typing_extensions import Never, NotRequired, TypedDict


class LRSchedulerMetadata(TypedDict):
    interval: Literal["epoch", "step"]
    """Interval to update the learning rate."""

    name: NotRequired[str | None]
    """Name of the learning rate scheduler. Default is `None`."""

    frequency: NotRequired[int]
    """Frequency to update the learning rate. Default is `1`."""

    reduce_on_plateau: NotRequired[bool]
    """Whether to reduce the learning rate on plateau. Default is `False`."""

    monitor: NotRequired[str | None]
    """Value to monitor for reducing the learning rate on plateau. Required if `reduce_on_plateau` is `True`.
    Default is `None`."""

    strict: NotRequired[bool]
    """Whether to enforce that the monitor exists for reducing the learning rate on plateau. Default is `True`."""


class LRSchedulerConfigBase(C.Config, ABC):
    @abstractmethod
    def metadata(self) -> LRSchedulerMetadata: ...

    @abstractmethod
    def create_scheduler_impl(
        self, optimizer: Optimizer, lightning_module: LightningModule
    ) -> LRSchedulerTypeUnion | LRSchedulerConfigType: ...

    def create_scheduler(
        self,
        optimizer: Optimizer,
        lightning_module: LightningModule,
        lr: Never
        | None = None,  # Backward compatibility, should be removed in the future
    ) -> LRSchedulerConfigType:
        # Create the scheduler.
        scheduler = self.create_scheduler_impl(optimizer, lightning_module)

        # If the scheduler is not a `LRSchedulerConfigType`, then make it one.
        if not isinstance(scheduler, Mapping):
            scheduler = LRSchedulerConfigType(scheduler=scheduler)

        # Update the scheduler config with the metadata (if not already present).
        metadata = self.metadata()
        # - `interval` has to be present.
        if scheduler.get("interval") is None:
            scheduler["interval"] = metadata["interval"]
        # - `name`
        if scheduler.get("name") is None and "name" in metadata:
            scheduler["name"] = metadata["name"]
        # - `frequency`
        if scheduler.get("frequency") is None and "frequency" in metadata:
            scheduler["frequency"] = metadata["frequency"]
        # - `reduce_on_plateau`
        if (
            scheduler.get("reduce_on_plateau") is None
            and "reduce_on_plateau" in metadata
        ):
            scheduler["reduce_on_plateau"] = metadata["reduce_on_plateau"]
        # - `monitor`
        if scheduler.get("monitor") is None and "monitor" in metadata:
            scheduler["monitor"] = metadata["monitor"]
        # - `strict`
        if scheduler.get("strict") is None and "strict" in metadata:
            scheduler["strict"] = metadata["strict"]  # type: ignore

        return scheduler

    def compute_num_steps_per_epoch(self, lightning_module: LightningModule) -> int:
        trainer = lightning_module.trainer
        # Use the Lightning trainer to convert the epoch-based values to step-based values
        _ = trainer.estimated_stepping_batches
        # ^ This is a hack to trigger the computation of the estimated stepping batches
        #   and make sure that the `trainer.num_training_batches` attribute is set.
        return math.ceil(trainer.num_training_batches / trainer.accumulate_grad_batches)


lr_scheduler_registry = C.Registry(LRSchedulerConfigBase, discriminator="name")
