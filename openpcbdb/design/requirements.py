from __future__ import annotations

from typing import Any

from openpcbdb.errors import ReferenceError


class DesignRequirementsMixin:
    """Requirements access API for design.openPCBDB."""

    def readRequirements(self) -> dict[str, Any]:
        """Read requirements.db through requirementsRef."""
        return self.requirements()

    def readRequirementsRef(self) -> dict[str, Any]:
        """Read requirementsRef from design.openPCBDB."""
        ref = self.data.get("requirementsRef")
        if not isinstance(ref, dict):
            raise ReferenceError("Design has no requirementsRef")
        return dict(ref)

    def setRequirementsRef(
        self,
        file: str,
        id: str,
        version: str,
        hash: str | None = None,
    ) -> None:
        """Set requirementsRef in design.openPCBDB."""
        ref: dict[str, Any] = {
            "file": file,
            "id": id,
            "version": version,
        }
        if hash is not None:
            ref["hash"] = hash
        self.data["requirementsRef"] = ref
        self.save()
