from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import nshconfig as C
from lightning.fabric.plugins import CheckpointIO, ClusterEnvironment
from lightning.pytorch.plugins.layer_sync import LayerSync
from lightning.pytorch.plugins.precision.precision import Precision
from typing_extensions import TypeAliasType

if TYPE_CHECKING:
    from .._config import TrainerConfig


Plugin = TypeAliasType(
    "Plugin", Precision | ClusterEnvironment | CheckpointIO | LayerSync
)


class PluginConfigBase(C.Config, ABC):
    @abstractmethod
    def create_plugin(self, trainer_config: "TrainerConfig") -> Plugin: ...


plugin_registry = C.Registry(PluginConfigBase, discriminator="name")
