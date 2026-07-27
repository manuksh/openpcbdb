from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol


class DbStore(Protocol):
    """Storage interface for OpenPCBDB database files."""

    def readObject(self, path: Path) -> dict[str, Any]:
        """Read a database object."""
        ...

    def writeObject(self, path: Path, data: dict[str, Any]) -> None:
        """Write a database object."""
        ...
