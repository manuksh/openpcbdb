from __future__ import annotations

from typing import Any

from .base import View


class BomView(View):
    """BOM view API."""

    def readItems(self) -> list[dict[str, Any]]:
        """Read BOM items."""
        items = self.data.get("items", [])
        return list(items) if isinstance(items, list) else []

    def addItem(self, item: dict[str, Any]) -> dict[str, Any]:
        """Add a BOM item."""
        items = self.readItems()
        items.append(item)
        self.data["items"] = items
        self.save()
        return item
