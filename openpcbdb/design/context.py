from __future__ import annotations

from typing import Any


class DesignContextMixin:
    """Bulk semantic context API for AI agents."""

    def readDesignContext(
        self,
        depth: int = 0,
        include: list[str] | None = None,
        maxTokens: int | None = None,
    ) -> dict[str, Any]:
        """Read a compact design-level context object for AI agents.

        Args:
            depth: Hierarchy depth to include from the top cell.
            include: Optional sections to include.
            maxTokens: Reserved for future context compression.
        """
        sections = set(include or ["properties", "requirementsRef", "libraries", "top"])
        context: dict[str, Any] = {}

        if "properties" in sections:
            context["properties"] = self.readDesignProperties()
        if "requirementsRef" in sections:
            context["requirementsRef"] = self.data.get("requirementsRef")
        if "requirements" in sections:
            context["requirements"] = self.readRequirements()
        if "libraries" in sections:
            context["libraries"] = self.data.get("libraries", [])
        if "top" in sections:
            context["top"] = self.data.get("top")
        if depth > 0:
            top = self.data.get("top", {})
            if isinstance(top, dict):
                libName = top.get("library")
                cellName = top.get("cell")
                if isinstance(libName, str) and isinstance(cellName, str):
                    context["topCellContext"] = self.readCellContext(
                        libName=libName,
                        cellName=cellName,
                        depth=depth - 1,
                    )
        if maxTokens is not None:
            context["maxTokens"] = maxTokens
        return context

    def readCellContext(
        self,
        libName: str,
        cellName: str,
        depth: int = 0,
        include: list[str] | None = None,
    ) -> dict[str, Any]:
        """Read a compact cell-level context object for AI agents."""
        sections = set(include or ["cell", "views"])
        cell = self.readCell(libName, cellName)
        context: dict[str, Any] = {
            "library": libName,
            "cell": cellName,
        }

        if "cell" in sections:
            context["cellProperties"] = cell.read_properties()
        if "views" in sections:
            context["views"] = cell.views
        if "symbol" in sections and "symbol" in cell.views:
            context["symbol"] = self.readViewProperties(libName, cellName, "symbol")
        if "schematic" in sections and "schematic" in cell.views:
            context["schematic"] = self.readViewProperties(libName, cellName, "schematic")
        if "layout" in sections and "layout" in cell.views:
            context["layout"] = self.readViewProperties(libName, cellName, "layout")
        if "constraints" in sections:
            context["constraints"] = self.readCellConstraints(libName, cellName)
        if depth > 0:
            context["children"] = self.readChildCellContexts(libName, cellName, depth=depth - 1)
        return context

    def readViewContext(
        self,
        libName: str,
        cellName: str,
        viewName: str,
        include: list[str] | None = None,
    ) -> dict[str, Any]:
        """Read a compact view-level context object for AI agents."""
        view = self.readView(libName, cellName, viewName)
        sections = set(include or ["properties", "constraints", "toolViews"])
        context: dict[str, Any] = {
            "library": libName,
            "cell": cellName,
            "view": viewName,
        }
        if "properties" in sections:
            context["properties"] = view.read_properties()
        if "constraints" in sections:
            context["constraints"] = view.constraints
        if "toolViews" in sections:
            context["toolViews"] = view.tool_views
        return context

    def readHierarchyContext(
        self,
        libName: str,
        cellName: str,
        depth: int = 1,
    ) -> dict[str, Any]:
        """Read hierarchy context starting from one cell."""
        return self.readCellContext(libName=libName, cellName=cellName, depth=depth)

    def readCellConstraints(self, libName: str, cellName: str) -> list[dict[str, Any]]:
        """Read all view-local constraints for a cell."""
        cell = self.readCell(libName, cellName)
        constraints: list[dict[str, Any]] = []
        for viewName in cell.views:
            view = self.readView(libName, cellName, viewName)
            for constraint in view.constraints:
                item = dict(constraint)
                item.setdefault("view", viewName)
                constraints.append(item)
        return constraints

    def readChildCellContexts(
        self,
        libName: str,
        cellName: str,
        depth: int = 0,
    ) -> list[dict[str, Any]]:
        """Read child cell contexts from schematic CellInstance objects."""
        try:
            schematic = self.readViewProperties(libName, cellName, "schematic")
        except Exception:
            return []

        children: list[dict[str, Any]] = []
        instances = schematic.get("instances", [])
        if not isinstance(instances, list):
            return children

        for inst in instances:
            if not isinstance(inst, dict) or inst.get("type") != "CellInstance":
                continue
            childLib = inst.get("library")
            childCell = inst.get("cell")
            if isinstance(childLib, str) and isinstance(childCell, str):
                children.append(
                    self.readCellContext(
                        libName=childLib,
                        cellName=childCell,
                        depth=depth,
                        include=["cell", "views", "symbol"],
                    )
                )
        return children
