from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

from typing_extensions import final, override

from .._callback import NTCallbackBase
from .base import CallbackConfigBase, callback_registry

log = logging.getLogger(__name__)


@final
@callback_registry.register
class DirectorySetupCallbackConfig(CallbackConfigBase):
    name: Literal["directory_setup"] = "directory_setup"

    enabled: bool = True
    """Whether to enable the directory setup callback."""

    create_symlink_to_nshrunner_root: bool = True
    """Should we create a symlink to the root folder for the Runner (if we're in one)?"""

    def __bool__(self):
        return self.enabled

    @override
    def create_callbacks(self, trainer_config):
        if not self:
            return

        yield DirectorySetupCallback(self)


def _create_symlink_to_nshrunner(base_dir: Path):
    try:
        import nshrunner as nr
    except ImportError:
        log.info("nshrunner is not installed. Skipping symlink creation to nshrunner.")
        return

    # Check if we are in a nshrunner session
    if (session := nr.Session.from_current_session()) is None:
        log.info("No current nshrunner session found. Skipping symlink creation.")
        return

    session_dir = session.session_dir
    if not session_dir.exists() or not session_dir.is_dir():
        log.warning(
            f"nshrunner's session_dir is not a valid directory: {session_dir}. "
            "Skipping symlink creation."
        )
        return

    # Create the symlink
    symlink_path = base_dir / "nshrunner"
    if symlink_path.exists(follow_symlinks=False):
        # If it already points to the correct directory, we're done
        if symlink_path.resolve() == session_dir.resolve():
            return

        # Otherwise, we should log a warning and remove the existing symlink
        log.warning(
            f"A symlink pointing to {symlink_path.resolve()} already exists at {symlink_path}. "
            "Removing the existing symlink."
        )
        symlink_path.unlink()

    symlink_path.symlink_to(session_dir, target_is_directory=True)


class DirectorySetupCallback(NTCallbackBase):
    @override
    def __init__(self, config: DirectorySetupCallbackConfig):
        super().__init__()

        self.config = config
        del config

    @override
    def setup(self, trainer, pl_module, stage):
        super().setup(trainer, pl_module, stage)

        # Create a symlink to the root folder for the Runner
        if self.config.create_symlink_to_nshrunner_root:
            base_dir = trainer.hparams.directory.resolve_run_root_directory(
                trainer.hparams.id
            )
            _create_symlink_to_nshrunner(base_dir)
