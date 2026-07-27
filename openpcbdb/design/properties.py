from __future__ import annotations

from typing import Any


class DesignPropertiesMixin:
    """Design property API for design.openPCBDB."""

    def readDesignProperties(self) -> dict[str, Any]:
        """Read all design.openPCBDB properties."""
        return dict(self.data)

    def updateDesignProperties(self, properties: dict[str, Any]) -> None:
        """Update design.openPCBDB properties and save the design index."""
        self.data.update(properties)
        self.save()

    def readDesignId(self) -> str:
        """Read the design id."""
        return str(self.data.get("id", ""))

    def readDesignName(self) -> str:
        """Read the design name."""
        return str(self.data.get("name", ""))

    def readDesignVersion(self) -> str:
        """Read the design version."""
        return str(self.data.get("version", ""))

    def setDesignVersion(self, version: str) -> None:
        """Set the design version and save the design index."""
        self.data["version"] = version
        self.save()

    def readDesignIndex(self) -> dict[str, Any]:
        """Read the design.openPCBDB index."""
        return self.readDesignProperties()
