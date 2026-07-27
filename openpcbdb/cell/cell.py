from __future__ import annotations

from pathlib import Path
from typing import Any

from openpcbdb.errors import ReferenceError
from openpcbdb.io import loadJsonFile, saveJsonFile
from openpcbdb.model import Cell as ModelCell
from openpcbdb.views import (
    BomView,
    LayoutView,
    ManufacturingView,
    NetlistView,
    SchematicView,
    SpiceView,
    SymbolView,
    VerilogView,
    View,
)

from .hierarchy import CellHierarchyMixin
from .properties import CellPropertiesMixin


class Cell(CellPropertiesMixin, CellHierarchyMixin, ModelCell):
    """EDA cell object."""

    @classmethod
    def load(cls, library: Any, path: Path) -> "Cell":
        """Load a cell object from cell.db."""
        data = loadJsonFile(path)
        cellName = data.get("cell")
        if not isinstance(cellName, str) or not cellName:
            raise ReferenceError(f"Cell file has no cell name: {path}")
        return cls(library=library, name=cellName, path=path, data=data)

    def readViews(self) -> dict[str, dict[str, Any]]:
        """Read declared views from cell.db."""
        return dict(self.views)

    def readView(self, viewName: str) -> View:
        """Read one typed view object."""
        return self.view(viewName)

    def view(self, name: str) -> View:
        viewRef = self.views.get(name)
        if not isinstance(viewRef, dict):
            raise ReferenceError(f"Cell {self.library.name}/{self.name} has no view {name!r}")
        pathValue = viewRef.get("path")
        if not isinstance(pathValue, str):
            raise ReferenceError(f"Cell {self.library.name}/{self.name} view {name!r} has no path")
        path = (self.path.parent / pathValue).resolve()
        data = loadJsonFile(path)
        viewClass = _viewClassForName(name)
        return viewClass(cell=self, name=name, path=path, data=data)

    def createView(
        self,
        viewName: str,
        viewType: str | None = None,
        properties: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> View:
        """Create a view and update cell.db/design.openPCBDB."""
        if viewName in self.views and not overwrite:
            raise ReferenceError(f"Cell {self.library.name}/{self.name} already has view {viewName!r}")

        resolvedType = viewType or _defaultViewType(viewName)
        viewDir = self.path.parent / viewName
        viewPath = viewDir / "view.db"
        if viewPath.exists() and not overwrite:
            raise ReferenceError(f"View file already exists: {viewPath}")

        data: dict[str, Any] = {
            "openpcbdbVersion": self.data.get("openpcbdbVersion", "0.2.0"),
            "type": resolvedType,
            "library": self.library.name,
            "cell": self.name,
            "view": viewName,
            "version": self.data.get("version", "0.1.0"),
        }
        if properties:
            data.update(properties)

        saveJsonFile(viewPath, data)
        views = dict(self.views)
        views[viewName] = {
            "path": f"{viewName}/view.db",
            "type": resolvedType,
            "version": data.get("version", "0.1.0"),
        }
        self.data["views"] = views
        self.save()
        self.library.workspace._index_view(
            self.library.name,
            self.name,
            viewName,
            {
                "path": str(viewPath.resolve().relative_to(self.library.workspace.root)),
                "type": resolvedType,
                "version": data.get("version", "0.1.0"),
            },
        )
        self.library.workspace.save()
        return self.view(viewName)

    def save(self) -> None:
        """Save cell.db."""
        saveJsonFile(self.path, self.data)


def _defaultViewType(viewName: str) -> str:
    if viewName == "symbol":
        return "CellSymbol"
    if viewName == "schematic":
        return "Schematic"
    if viewName == "layout":
        return "PCBLayout"
    if viewName == "bom":
        return "Bom"
    if viewName == "netlist":
        return "Netlist"
    return "View"


def _viewClassForName(viewName: str) -> type[View]:
    if viewName == "symbol":
        return SymbolView
    if viewName == "schematic":
        return SchematicView
    if viewName == "layout":
        return LayoutView
    if viewName == "netlist":
        return NetlistView
    if viewName == "bom":
        return BomView
    if viewName == "spice":
        return SpiceView
    if viewName == "verilog":
        return VerilogView
    if viewName == "manufacturing":
        return ManufacturingView
    return View
