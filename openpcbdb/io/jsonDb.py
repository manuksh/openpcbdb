from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonDbStore:
    """JSON storage implementation for OpenPCBDB .db files.

    The current OpenPCBDB database structure is stored as JSON files.
    Future storage implementations, such as SQLite, should implement the
    same readObject/writeObject interface.
    """

    def readObject(self, path: Path) -> dict[str, Any]:
        """Read one JSON database object from disk."""
        return loadJsonFile(path)

    def writeObject(self, path: Path, data: dict[str, Any]) -> None:
        """Write one JSON database object to disk."""
        saveJsonFile(path, data)


def loadJsonFile(path: Path) -> dict[str, Any]:
    """Load a JSON object from disk."""
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def saveJsonFile(path: Path, data: dict[str, Any]) -> None:
    """Save a JSON object to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")
