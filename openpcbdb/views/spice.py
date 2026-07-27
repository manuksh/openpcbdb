from __future__ import annotations

from .base import View


class SpiceView(View):
    """SPICE view API."""

    def readNetlistPath(self) -> str:
        """Read SPICE netlist path."""
        return str(self.data.get("netlistPath", ""))
