from __future__ import annotations

from typing import Any

from openpcbdb.io import saveJsonFile
from openpcbdb.model import View as ModelView


class View(ModelView):
    """Base EDA view object."""

    def readProperties(self) -> dict[str, Any]:
        """Read all view properties."""
        return dict(self.data)

    def updateProperties(self, properties: dict[str, Any]) -> None:
        """Update view properties and save view.db."""
        self.data.update(properties)
        self.save()

    def readConstraints(self) -> list[dict[str, Any]]:
        """Read view-local constraints."""
        return list(self.constraints)

    def readConstraint(self, constraintName: str) -> dict[str, Any]:
        """Read one view-local constraint by id."""
        for constraint in self.constraints:
            if constraint.get("id") == constraintName:
                return dict(constraint)
        raise KeyError(f"Constraint not found: {constraintName}")

    def createConstraint(
        self,
        constraintName: str,
        constraintType: str,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a view-local constraint."""
        constraints = list(self.constraints)
        constraint: dict[str, Any] = {
            "id": constraintName,
            "type": constraintType,
        }
        if properties:
            constraint.update(properties)
        constraints.append(constraint)
        self.data["constraints"] = constraints
        self.save()
        return constraint

    def updateConstraint(self, constraintName: str, properties: dict[str, Any]) -> None:
        """Update a view-local constraint."""
        constraints = list(self.constraints)
        for constraint in constraints:
            if constraint.get("id") == constraintName:
                constraint.update(properties)
                self.data["constraints"] = constraints
                self.save()
                return
        raise KeyError(f"Constraint not found: {constraintName}")

    def deleteConstraint(self, constraintName: str) -> None:
        """Delete a view-local constraint."""
        constraints = [
            constraint for constraint in self.constraints if constraint.get("id") != constraintName
        ]
        self.data["constraints"] = constraints
        self.save()

    def readToolViews(self) -> list[dict[str, Any]]:
        """Read tool-specific EDA view representations."""
        return list(self.tool_views)

    def readToolView(self, tool: str) -> dict[str, Any]:
        """Read one toolView by tool name."""
        for toolView in self.tool_views:
            if toolView.get("tool") == tool:
                return dict(toolView)
        raise KeyError(f"ToolView not found: {tool}")

    def createToolView(
        self,
        tool: str,
        format: str,
        path: str,
        role: str = "derived",
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a toolView entry."""
        toolViews = [item for item in self.tool_views if item.get("tool") != tool]
        toolView: dict[str, Any] = {
            "tool": tool,
            "format": format,
            "path": path,
            "role": role,
        }
        if properties:
            toolView.update(properties)
        toolViews.append(toolView)
        self.data["toolViews"] = toolViews
        self.save()
        return toolView

    def updateToolView(self, tool: str, properties: dict[str, Any]) -> None:
        """Update one toolView entry."""
        toolViews = list(self.tool_views)
        for toolView in toolViews:
            if toolView.get("tool") == tool:
                toolView.update(properties)
                self.data["toolViews"] = toolViews
                self.save()
                return
        raise KeyError(f"ToolView not found: {tool}")

    def deleteToolView(self, tool: str) -> None:
        """Delete one toolView entry."""
        self.data["toolViews"] = [item for item in self.tool_views if item.get("tool") != tool]
        self.save()

    def save(self) -> None:
        """Save view.db."""
        saveJsonFile(self.path, self.data)
