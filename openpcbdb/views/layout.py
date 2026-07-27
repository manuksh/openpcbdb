from __future__ import annotations

from typing import Any

from .base import View


class LayoutView(View):
    """Layout view API for physical implementation."""

    def readPlacements(self) -> list[dict[str, Any]]:
        """Read component or cell placements."""
        placements = self.data.get("placements", [])
        return list(placements) if isinstance(placements, list) else []

    def createPlacement(
        self,
        targetName: str,
        x: float,
        y: float,
        unit: str = "mm",
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a placement entry."""
        placements = self.readPlacements()
        placement: dict[str, Any] = {
            "position": {
                "x": x,
                "y": y,
                "unit": unit,
            }
        }
        if targetName.startswith("X_"):
            placement["instance"] = targetName
        else:
            placement["refDesignator"] = targetName
        if properties:
            placement.update(properties)
        placements.append(placement)
        self.data["placements"] = placements
        self.save()
        return placement

    def readRoutes(self) -> list[dict[str, Any]]:
        """Read routing objects."""
        routing = self.data.get("routing", [])
        return list(routing) if isinstance(routing, list) else []

    def readZones(self) -> list[dict[str, Any]]:
        """Read copper zones."""
        zones = self.data.get("zones", [])
        return list(zones) if isinstance(zones, list) else []

    def readDrc(self) -> dict[str, Any]:
        """Read DRC status."""
        drc = self.data.get("drc", {})
        return dict(drc) if isinstance(drc, dict) else {}
