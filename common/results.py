"""Helpers for logging runs and comparing with the paper."""
from __future__ import annotations

import csv
import datetime as _dt
from pathlib import Path


def log_run(results_dir, **fields) -> Path:
    """Append one row (with a timestamp) to results/runs.csv."""
    path = Path(results_dir) / "runs.csv"
    row = {"timestamp": _dt.datetime.now().isoformat(timespec="seconds"), **fields}
    new = not path.exists()
    with path.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row))
        if new:
            writer.writeheader()
        writer.writerow(row)
    return path


def compare_with_paper(rows, save_to=None):
    """rows: list of dicts with Metric, Paper, Mine (+ any extra columns).

    Returns a pandas DataFrame with a Gap column; optionally saves it as CSV.
    """
    import pandas as pd

    df = pd.DataFrame(rows)
    df["Gap"] = pd.to_numeric(df.get("Mine"), errors="coerce") - pd.to_numeric(df.get("Paper"), errors="coerce")
    if save_to is not None:
        df.to_csv(save_to, index=False)
    return df
