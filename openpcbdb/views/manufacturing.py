from __future__ import annotations

from typing import Any

from .base import View


class ManufacturingView(View):
    """Manufacturing view API."""

    def readOutputs(self) -> list[dict[str, Any]]:
        """Read manufacturing output artifacts."""
        outputs = self.data.get("outputs", [])
        return list(outputs) if isinstance(outputs, list) else []
