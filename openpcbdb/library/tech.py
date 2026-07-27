from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openpcbdb.io import loadJsonFile, saveJsonFile


@dataclass
class Tech:
    """Technology database object."""

    lib: Any
    path: Path
    data: dict[str, Any]

    @classmethod
    def load(cls, lib: Any, path: Path) -> "Tech":
        """Load technology.db."""
        return cls(lib=lib, path=path, data=loadJsonFile(path))

    def readProperties(self) -> dict[str, Any]:
        """Read technology.db properties."""
        return dict(self.data)

    def updateProperties(self, properties: dict[str, Any]) -> None:
        """Update technology.db properties."""
        self.data.update(properties)
        self.save()

    def readDesignRules(self) -> dict[str, Any]:
        """Read technology design rules."""
        rules = self.data.get("designRules", {})
        return dict(rules) if isinstance(rules, dict) else {}

    def readStackup(self) -> dict[str, Any]:
        """Read technology stackup."""
        stackup = self.data.get("stackup", {})
        return dict(stackup) if isinstance(stackup, dict) else {}

    def save(self) -> None:
        """Save technology.db."""
        saveJsonFile(self.path, self.data)
