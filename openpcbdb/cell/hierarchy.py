from __future__ import annotations

from typing import Any


class CellHierarchyMixin:
    """Cell hierarchy helpers."""

    def readChildInsts(self) -> list[dict[str, Any]]:
        """Read child CellInstance objects from schematic view."""
        try:
            schematic = self.readView("schematic")
        except Exception:
            return []
        instances = schematic.data.get("instances", [])
        if not isinstance(instances, list):
            return []
        return [inst for inst in instances if isinstance(inst, dict) and inst.get("type") == "CellInstance"]

    def readChildCells(self) -> list[tuple[str, str]]:
        """Read referenced child cells as (libName, cellName)."""
        children: list[tuple[str, str]] = []
        for inst in self.readChildInsts():
            libName = inst.get("library")
            cellName = inst.get("cell")
            if isinstance(libName, str) and isinstance(cellName, str):
                children.append((libName, cellName))
        return children
