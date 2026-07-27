from __future__ import annotations

from typing import Any


class LibraryIndexMixin:
    """library.db index operations."""

    def readProperties(self) -> dict[str, Any]:
        """Read library.db properties."""
        return dict(self.data)

    def readCells(self) -> list[dict[str, Any]]:
        """Read cells listed in library.db."""
        return list(self.cells)

    def readCellIndex(self, cellName: str) -> dict[str, Any]:
        """Read one cell index entry."""
        for cellRef in self.cells:
            if cellRef.get("cell") == cellName:
                return dict(cellRef)
        raise KeyError(f"Cell not found in library index: {cellName}")

    def readTechnologyRef(self) -> dict[str, Any]:
        """Read technologyRef from library.db."""
        ref = self.data.get("technologyRef", {})
        return dict(ref) if isinstance(ref, dict) else {}
