from __future__ import annotations

from typing import Any

from .base import View


class NetlistView(View):
    """Netlist view API."""

    def readNets(self) -> list[dict[str, Any]]:
        """Read netlist nets."""
        nets = self.data.get("nets", [])
        return list(nets) if isinstance(nets, list) else []

    def readEntries(self) -> list[dict[str, Any]]:
        """Read raw netlist entries."""
        entries = self.data.get("entries", [])
        return list(entries) if isinstance(entries, list) else []
