from __future__ import annotations

from .base import View


class VerilogView(View):
    """Verilog view API."""

    def readModulePath(self) -> str:
        """Read Verilog module path."""
        return str(self.data.get("modulePath", ""))
