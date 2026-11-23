#!/usr/bin/env python3
"""Build the student version of a paper notebook.

Removes every cell tagged `solution` and clears all outputs.

Usage (from the repo root):
    python tools/make_student_version.py trackA_classical/03_random_forests/notebook.ipynb
Writes: teaching/student_notebooks/03_random_forests.ipynb
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(src: str) -> None:
    src_path = Path(src)
    nb = json.loads(src_path.read_text(encoding="utf-8"))
    kept = []
    for cell in nb["cells"]:
        if "solution" in cell.get("metadata", {}).get("tags", []):
            continue
        if cell["cell_type"] == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
        kept.append(cell)
    nb["cells"] = kept
    out = ROOT / "teaching" / "student_notebooks" / f"{src_path.resolve().parent.name}.ipynb"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
