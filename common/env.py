"""Environment setup: seeds, platform detection, library versions, GPU info."""
from __future__ import annotations

import importlib
import os
import platform
import random
import sys


def _version(module_name: str):
    try:
        return importlib.import_module(module_name).__version__
    except Exception:
        return None


def setup_env(seed: int = 42, deterministic: bool = False, verbose: bool = True) -> dict:
    """Seed every RNG we use and report the environment.

    Returns a dict you can paste into the notebook's Implementation notes.
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass

    gpus = []
    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
        if deterministic:
            tf.config.experimental.enable_op_determinism()
        gpus = [d.name for d in tf.config.list_physical_devices("GPU")]
    except ImportError:
        pass
    try:
        import torch  # only once the PyTorch port phase starts
        torch.manual_seed(seed)
    except ImportError:
        pass

    info = {
        "platform": "colab" if "google.colab" in sys.modules
        else "kaggle" if "KAGGLE_KERNEL_RUN_TYPE" in os.environ else "local",
        "python": platform.python_version(),
        "machine": f"{platform.system()} {platform.machine()}",
        "seed": seed,
        "gpus": gpus,
    }
    for name in ["numpy", "pandas", "sklearn", "tensorflow", "keras", "cv2", "xgboost", "torch"]:
        v = _version(name)
        if v:
            info[name] = v
    if verbose:
        for k, v in info.items():
            print(f"{k:>11}: {v}")
    return info
