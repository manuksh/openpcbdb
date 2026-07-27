from __future__ import annotations

import argparse
from pathlib import Path

from .design import OpenPCBDB


def main() -> int:
    parser = argparse.ArgumentParser(prog="openpcbdb-validate")
    parser.add_argument("project", help="Path to design.openPCBDB or its workspace directory")
    args = parser.parse_args()

    db = OpenPCBDB.open(Path(args.project))
    report = db.checkDesign()

    for result in report.results:
        location = f" ({result.path})" if result.path else ""
        print(f"{result.severity.upper()}: {result.message}{location}")

    if report.ok:
        print("OK: workspace valid")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
