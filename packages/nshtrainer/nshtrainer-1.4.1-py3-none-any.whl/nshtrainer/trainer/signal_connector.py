from __future__ import annotations

import logging
import os
import platform
import re
import signal
import subprocess
import sys
import threading
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from types import FrameType
from typing import Any

import torch.utils.data
from lightning.fabric.plugins.environments.lsf import LSFEnvironment
from lightning.fabric.plugins.environments.slurm import SLURMEnvironment
from lightning.pytorch.trainer.connectors.signal_connector import _HandlersCompose
from lightning.pytorch.trainer.connectors.signal_connector import (
    _SignalConnector as _LightningSignalConnector,
)
from typing_extensions import TypeAliasType, override

log = logging.getLogger(__name__)

_SIGNUM = TypeAliasType("_SIGNUM", int | signal.Signals)
_HANDLER = TypeAliasType(
    "_HANDLER", Callable[[_SIGNUM, FrameType], Any] | int | signal.Handlers | None
)
_IS_WINDOWS = platform.system() == "Windows"


def _resolve_requeue_signals():
    try:
        import nshrunner as nr
    except ImportError:
        log.debug("nshrunner not found. Skipping signal requeueing.")
        return None

    if (session := nr.Session.from_current_session()) is None:
        return None

    signals: list[signal.Signals] = []
    if session.submit_timeout_signal:
        signals.append(session.submit_timeout_signal)
    if session.submit_preempt_signal:
        signals.append(session.submit_preempt_signal)
    return signals


class _SignalConnector(_LightningSignalConnector):
    def _auto_requeue_signals(self) -> list[signal.Signals] | None:
        if not (signals := _resolve_requeue_signals()):
            return None

        signals_set = set(signals)
        valid_signals: set[signal.Signals] = signal.valid_signals()
        assert signals_set.issubset(valid_signals), (
            f"Invalid signal(s) found: {signals_set - valid_signals}"
        )
        return signals

    def _compose_and_register(
        self,
        signum: signal.Signals,
        handlers: list[_HANDLER],
        replace_existing: bool = False,
    ):
        if _IS_WINDOWS:
            log.info(
                f"Signal {signum.name} has no handlers or is not supported on Windows."
            )
            return

        if self._has_already_handler(signum):
            if not replace_existing:
                log.info(
                    f"Signal {signum.name} already has a handler. Adding ours to the existing one."
                )
                handlers.append(signal.getsignal(signum))
            else:
                log.info(
                    f"Replacing existing handler for signal {signum.name} with ours."
                )

        self._register_signal(signum, _HandlersCompose(handlers))
        log.info(f"Registered {len(handlers)} handlers for signal {signum.name}.")

    @override
    def register_signal_handlers(self) -> None:
        if not (auto_requeue_signals := self._auto_requeue_signals()):
            log.info(
                "No auto-requeue signals found. Reverting to default Lightning behavior."
            )
            return super().register_signal_handlers()

        self.received_sigterm = False
        self._original_handlers = self._get_current_signal_handlers()

        signals = defaultdict[signal.Signals, list[_HANDLER]](lambda: [])
        signals[signal.SIGTERM].append(self._sigterm_notifier_fn)

        environment = self.trainer._accelerator_connector.cluster_environment
        if isinstance(environment, SLURMEnvironment):
            log.info("SLURM auto-requeueing enabled. Setting signal handlers.")
            for signal_handler in auto_requeue_signals:
                signals[signal_handler].append(self._slurm_sigusr_handler_fn)

        if isinstance(environment, LSFEnvironment):
            # Important note from https://amrex-astro.github.io/workflow/olcf-workflow.html:
            # We can also ask the job manager to send a warning signal some amount of time before the allocation expires by passing -wa 'signal' and -wt '[hour:]minute' to bsub. We can then have bash create a dump_and_stop file when it receives the signal, which will tell Castro to output a checkpoint file and exit cleanly after it finishes the current timestep. An important detail that I couldn't find documented anywhere is that the job manager sends the signal to all the processes in the job, not just the submission script, and we have to use a signal that is ignored by default so Castro doesn't immediately crash upon receiving it. SIGCHLD, SIGURG, and SIGWINCH are the only signals that fit this requirement and of these, SIGURG is the least likely to be triggered by other events.

            log.info("LSF auto-requeueing enabled. Setting signal handlers.")
            for signal_handler in auto_requeue_signals:
                signals[signal_handler].append(self._lsf_sigusr_handler_fn)

        for signum, handlers in signals.items():
            if not handlers:
                continue

            self._compose_and_register(signum, handlers)

    def _should_ignore_signal_handler(self) -> str | None:
        if threading.current_thread() is not threading.main_thread():
            return "Not in main thread"

        if torch.utils.data.get_worker_info() is not None:
            return "Inside DataLoader worker process"

        return None

    @override
    def _slurm_sigusr_handler_fn(self, signum: _SIGNUM, _: FrameType) -> None:
        if ignore_reason := self._should_ignore_signal_handler():
            log.info(
                f"Skipping SLURM auto-requeue signal handler. Reason: {ignore_reason}"
            )
            return

        log.critical(f"Handling SLURM auto-requeue signal: {signum}")

        # save logger to make sure we get all the metrics
        for logger in self.trainer.loggers:
            logger.finalize("finished")

        hpc_save_path = self.trainer._checkpoint_connector.hpc_save_path(
            self.trainer.default_root_dir
        )
        self.trainer.save_checkpoint(hpc_save_path)

        if not self.trainer.is_global_zero:
            return

        # find job id
        array_job_id = os.getenv("SLURM_ARRAY_JOB_ID")
        if array_job_id is not None:
            array_task_id = os.environ["SLURM_ARRAY_TASK_ID"]
            job_id = f"{array_job_id}_{array_task_id}"
        else:
            job_id = os.environ["SLURM_JOB_ID"]

        assert re.match("[0-9_-]+", job_id)
        cmd = ["scontrol", "requeue", job_id]

        # requeue job
        log.info(f"Requeuing job {job_id}...")
        try:
            result = subprocess.call(cmd)
        except FileNotFoundError:
            # This can occur if a subprocess call to `scontrol` is run outside a shell context
            # Re-attempt call (now with shell context). If any error is raised, propagate to user.
            # When running a shell command, it should be passed as a single string.
            result = subprocess.call(" ".join(cmd), shell=True)

        # print result text
        if result == 0:
            log.info(f"Requeued SLURM job: {job_id}")
        else:
            log.warning(f"Requeuing SLURM job {job_id} failed with error code {result}")

    def _lsf_sigusr_handler_fn(self, signum: _SIGNUM, _: FrameType) -> None:
        if ignore_reason := self._should_ignore_signal_handler():
            log.info(
                f"Skipping LSF auto-requeue signal handler. Reason: {ignore_reason}"
            )
            return

        log.critical(f"Handling LSF auto-requeue signal: {signum}")

        # Save logger to make sure we get all the metrics
        for logger in self.trainer.loggers:
            logger.finalize("finished")

        # Save checkpoint
        hpc_save_path = self.trainer._checkpoint_connector.hpc_save_path(
            self.trainer.default_root_dir
        )
        self.trainer.save_checkpoint(hpc_save_path)
        log.info(f"Saved checkpoint to {hpc_save_path}")

        if not self.trainer.is_global_zero:
            return

        # Find job id
        if (job_id := os.getenv("LSB_JOBID")) is None:
            log.warning(
                "LSB_JOBID environment variable not found. Unable to requeue job."
            )
            return

        assert re.match("[0-9_-]+", job_id)

        exe = "brequeue"
        if (bin_dir := os.getenv("LSF_BINDIR")) is not None:
            exe = str((Path(bin_dir) / exe).resolve().absolute())

        log.info(f"Using LSF requeue executable: {exe}")

        # If NSHRUNNER_LSF_EXIT_SCRIPT_DIR exists, we should emit a bash script in that directory
        # rather than calling the requeue command directly. This is because the requeue command
        # is only available outside of the `jsrun` context, and the exit script is called within
        # the `jsrun` context.
        if not (exit_script_dir := os.getenv("NSHRUNNER_LSF_EXIT_SCRIPT_DIR")):
            cmd = [exe, job_id]

            # Requeue job
            log.info(f"Requeuing job {job_id}...")
            try:
                result = subprocess.call(cmd)
            except FileNotFoundError:
                # Retry with shell context if subprocess call fails
                result = subprocess.call(" ".join(cmd), shell=True)

            # Print result text
            if result == 0:
                log.info(f"Requeued LSF job: {job_id}")
            else:
                log.warning(
                    f"Requeuing LSF job {job_id} failed with error code {result}"
                )
        else:
            log.critical(
                "Environment variable NSHRUNNER_LSF_EXIT_SCRIPT_DIR found.\n"
                "Writing requeue script to exit script directory."
            )
            exit_script_dir = Path(exit_script_dir)
            assert exit_script_dir.is_dir(), (
                f"Exit script directory {exit_script_dir} does not exist"
            )

            exit_script_path = exit_script_dir / f"requeue_{job_id}.sh"
            log.info(f"Writing requeue script to {exit_script_path}")

            with exit_script_path.open("w") as f:
                f.write(f"#!/bin/bash\n{exe} {job_id}\n")

            # Make the script executable
            os.chmod(exit_script_path, 0o755)

            log.info(f"Requeue script written to {exit_script_path}")

            # Kill the current session to trigger the exit script
            log.info("Killing current session to trigger exit script")
            self._kill_current_session()

    def _kill_current_session(self):
        from lightning.pytorch.trainer.call import _interrupt

        _interrupt(self.trainer, KeyboardInterrupt())
        self.trainer._teardown()
        if (launcher := self.trainer.strategy.launcher) is not None:
            launcher.kill(_get_sigkill_signal())
        exit(1)


def _get_sigkill_signal() -> _SIGNUM:
    return signal.SIGTERM if sys.platform == "win32" else signal.SIGKILL
