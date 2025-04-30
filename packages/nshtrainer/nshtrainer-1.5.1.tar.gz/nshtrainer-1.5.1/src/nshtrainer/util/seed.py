from __future__ import annotations

import logging

import lightning.fabric.utilities.seed as LS

log = logging.getLogger(__name__)


def seed_everything(seed: int | None, *, workers: bool = False):
    seed = LS.seed_everything(seed, workers=workers)
    log.critical(f"Set global seed to {seed}.")
    return seed
