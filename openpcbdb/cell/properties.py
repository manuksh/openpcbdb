from __future__ import annotations

from typing import Any


class CellPropertiesMixin:
    """Cell property API."""

    def readProperties(self) -> dict[str, Any]:
        """Read cell.db properties."""
        return dict(self.data)

    def updateProperties(self, properties: dict[str, Any]) -> None:
        """Update cell.db properties."""
        self.data.update(properties)
        self.save()

    def readCellName(self) -> str:
        """Read cell name."""
        return self.name

    def readCellType(self) -> str:
        """Read cell type."""
        return str(self.data.get("cellType", ""))
