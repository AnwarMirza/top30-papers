"""Plotting helpers shared by the notebooks."""
from __future__ import annotations

from pathlib import Path


def plot_history(history, metrics=("loss", "accuracy"), save_to=None):
    """Plot train/validation curves from a Keras History (or a dict of lists)."""
    import matplotlib.pyplot as plt

    hist = history.history if hasattr(history, "history") else history
    metrics = [m for m in metrics if m in hist]
    fig, axes = plt.subplots(1, len(metrics), figsize=(5 * len(metrics), 3.5), squeeze=False)
    for ax, m in zip(axes[0], metrics):
        ax.plot(hist[m], label=f"train {m}")
        if f"val_{m}" in hist:
            ax.plot(hist[f"val_{m}"], label=f"val {m}")
        ax.set_xlabel("epoch")
        ax.set_title(m)
        ax.legend()
    fig.tight_layout()
    if save_to is not None:
        savefig(fig, save_to)
    return fig


def savefig(fig, path, dpi: int = 150):
    """Save a figure, creating the folder if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return path
