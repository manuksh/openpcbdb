"""Draft OpenPCBDB public API surface.

This file is intentionally a planning artifact, not implementation code.
Public API names use camelBack style.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class OpenPCBDB:
    """Design database handle loaded from design.openPCBDB."""

    @classmethod
    def open(cls, path: str | Path) -> "OpenPCBDB":
        """Open design.openPCBDB or a directory containing design.openPCBDB."""
        raise NotImplementedError

    @classmethod
    def create(
        cls,
        path: str | Path,
        name: str,
        topCell: tuple[str, str, str] | None = None,
    ) -> "OpenPCBDB":
        """Create a new OpenPCBDB design database."""
        raise NotImplementedError

    def save(self) -> None:
        """Save design.openPCBDB and any dirty loaded objects."""
        raise NotImplementedError

    def reload(self) -> None:
        """Reload design.openPCBDB from disk."""
        raise NotImplementedError

    def close(self) -> None:
        """Close the design database handle."""
        raise NotImplementedError

    def validate(self) -> Any:
        """Validate the complete design database."""
        raise NotImplementedError

    def readDesignProperties(self) -> dict[str, Any]:
        """Read design.openPCBDB properties."""
        raise NotImplementedError

    def updateDesignProperties(self, properties: dict[str, Any]) -> None:
        """Update design.openPCBDB properties."""
        raise NotImplementedError

    def readDesignId(self) -> str:
        """Read design id."""
        raise NotImplementedError

    def readDesignName(self) -> str:
        """Read design name."""
        raise NotImplementedError

    def readDesignVersion(self) -> str:
        """Read design version."""
        raise NotImplementedError

    def setDesignVersion(self, version: str) -> None:
        """Set design version."""
        raise NotImplementedError

    def readRequirements(self) -> dict[str, Any]:
        """Read requirements.db."""
        raise NotImplementedError

    def readRequirementsRef(self) -> dict[str, Any]:
        """Read requirements reference from design.openPCBDB."""
        raise NotImplementedError

    def setRequirementsRef(
        self,
        file: str,
        id: str,
        version: str,
        hash: str | None = None,
    ) -> None:
        """Set requirements reference in design.openPCBDB."""
        raise NotImplementedError

    def readLibraries(self) -> list[dict[str, Any]]:
        """Read library index entries from design.openPCBDB."""
        raise NotImplementedError

    def readLibrary(self, library: str) -> Any:
        """Read a library handle."""
        raise NotImplementedError

    def readLibraryProperties(self, library: str) -> dict[str, Any]:
        """Read library.db properties."""
        raise NotImplementedError

    def createLibrary(
        self,
        library: str,
        technologyRef: dict[str, Any] | None = None,
        properties: dict[str, Any] | None = None,
    ) -> Any:
        """Create a library and add it to design.openPCBDB."""
        raise NotImplementedError

    def deleteLibrary(self, library: str) -> None:
        """Delete a library from the design database."""
        raise NotImplementedError

    def renameLibrary(self, oldName: str, newName: str) -> None:
        """Rename a library and update design.openPCBDB references."""
        raise NotImplementedError

    def readTechnology(self, library: str) -> dict[str, Any]:
        """Read technology.db for a library."""
        raise NotImplementedError

    def readTechnologyRef(self, library: str) -> dict[str, Any]:
        """Read technology reference for a library."""
        raise NotImplementedError

    def setTechnologyRef(
        self,
        library: str,
        file: str,
        id: str,
        version: str,
    ) -> None:
        """Set technology reference for a library."""
        raise NotImplementedError

    def createTechnology(
        self,
        library: str,
        id: str,
        name: str,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create technology.db for a library."""
        raise NotImplementedError

    def updateTechnology(self, library: str, properties: dict[str, Any]) -> None:
        """Update technology.db for a library."""
        raise NotImplementedError

    def readCells(self, library: str) -> list[dict[str, Any]]:
        """Read cell index entries for a library."""
        raise NotImplementedError

    def readCell(self, library: str, cell: str) -> Any:
        """Read a cell handle."""
        raise NotImplementedError

    def readCellProperties(self, library: str, cell: str) -> dict[str, Any]:
        """Read cell.db properties."""
        raise NotImplementedError

    def createCell(
        self,
        library: str,
        cell: str,
        cellType: str = "leaf",
        name: str | None = None,
        properties: dict[str, Any] | None = None,
    ) -> Any:
        """Create a cell and update library.db and design.openPCBDB."""
        raise NotImplementedError

    def deleteCell(self, library: str, cell: str) -> None:
        """Delete a cell from a library."""
        raise NotImplementedError

    def renameCell(self, library: str, oldCell: str, newCell: str) -> None:
        """Rename a cell and update references."""
        raise NotImplementedError

    def copyCell(
        self,
        srcLibrary: str,
        srcCell: str,
        dstLibrary: str,
        dstCell: str,
    ) -> Any:
        """Copy a cell from one library/cell name to another."""
        raise NotImplementedError

    def readViews(self, library: str, cell: str) -> dict[str, dict[str, Any]]:
        """Read view index entries for a cell."""
        raise NotImplementedError

    def readView(self, library: str, cell: str, view: str) -> Any:
        """Read a view handle."""
        raise NotImplementedError

    def readViewProperties(self, library: str, cell: str, view: str) -> dict[str, Any]:
        """Read view.db properties."""
        raise NotImplementedError

    def createView(
        self,
        library: str,
        cell: str,
        view: str,
        viewType: str | None = None,
        properties: dict[str, Any] | None = None,
    ) -> Any:
        """Create a view and update cell.db and design.openPCBDB."""
        raise NotImplementedError

    def deleteView(self, library: str, cell: str, view: str) -> None:
        """Delete a view from a cell."""
        raise NotImplementedError

    def renameView(
        self,
        library: str,
        cell: str,
        oldView: str,
        newView: str,
    ) -> None:
        """Rename a view and update references."""
        raise NotImplementedError

    def copyView(
        self,
        srcLibrary: str,
        srcCell: str,
        srcView: str,
        dstLibrary: str,
        dstCell: str,
        dstView: str,
    ) -> Any:
        """Copy a view between cells."""
        raise NotImplementedError

    def readPorts(self, library: str, cell: str) -> list[dict[str, Any]]:
        """Read ports from symbol/view.db."""
        raise NotImplementedError

    def readPort(self, library: str, cell: str, port: str) -> dict[str, Any]:
        """Read one port from symbol/view.db."""
        raise NotImplementedError

    def createPort(
        self,
        library: str,
        cell: str,
        port: str,
        direction: str,
        electricalType: str,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a port in symbol/view.db."""
        raise NotImplementedError

    def updatePort(
        self,
        library: str,
        cell: str,
        port: str,
        properties: dict[str, Any],
    ) -> None:
        """Update a port in symbol/view.db."""
        raise NotImplementedError

    def deletePort(self, library: str, cell: str, port: str) -> None:
        """Delete a port from symbol/view.db."""
        raise NotImplementedError

    def readInstances(self, library: str, cell: str) -> list[dict[str, Any]]:
        """Read instances from schematic/view.db."""
        raise NotImplementedError

    def readInstance(self, library: str, cell: str, instance: str) -> dict[str, Any]:
        """Read one instance from schematic/view.db."""
        raise NotImplementedError

    def createCellInstance(
        self,
        library: str,
        cell: str,
        instance: str,
        refLibrary: str,
        refCell: str,
        viewBinding: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create a CellInstance inside schematic/view.db."""
        raise NotImplementedError

    def createComponentInstance(
        self,
        library: str,
        cell: str,
        refDesignator: str,
        componentDefinitionId: str,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a ComponentInstance inside schematic/view.db."""
        raise NotImplementedError

    def updateInstance(
        self,
        library: str,
        cell: str,
        instance: str,
        properties: dict[str, Any],
    ) -> None:
        """Update an instance inside schematic/view.db."""
        raise NotImplementedError

    def deleteInstance(self, library: str, cell: str, instance: str) -> None:
        """Delete an instance from schematic/view.db."""
        raise NotImplementedError

    def readNets(
        self,
        library: str,
        cell: str,
        view: str = "schematic",
    ) -> list[dict[str, Any]]:
        """Read nets from a view."""
        raise NotImplementedError

    def readNet(
        self,
        library: str,
        cell: str,
        net: str,
        view: str = "schematic",
    ) -> dict[str, Any]:
        """Read one net from a view."""
        raise NotImplementedError

    def createNet(
        self,
        library: str,
        cell: str,
        net: str,
        name: str | None = None,
        view: str = "schematic",
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a net in a view."""
        raise NotImplementedError

    def connect(
        self,
        library: str,
        cell: str,
        net: str,
        connection: dict[str, Any],
        view: str = "schematic",
    ) -> None:
        """Add a connection to a net."""
        raise NotImplementedError

    def disconnect(
        self,
        library: str,
        cell: str,
        net: str,
        connection: dict[str, Any],
        view: str = "schematic",
    ) -> None:
        """Remove a connection from a net."""
        raise NotImplementedError

    def deleteNet(
        self,
        library: str,
        cell: str,
        net: str,
        view: str = "schematic",
    ) -> None:
        """Delete a net from a view."""
        raise NotImplementedError

    def readConstraints(
        self,
        library: str,
        cell: str,
        view: str,
    ) -> list[dict[str, Any]]:
        """Read constraints from a view."""
        raise NotImplementedError

    def readConstraint(
        self,
        library: str,
        cell: str,
        view: str,
        constraint: str,
    ) -> dict[str, Any]:
        """Read one constraint from a view."""
        raise NotImplementedError

    def createConstraint(
        self,
        library: str,
        cell: str,
        view: str,
        constraint: str,
        constraintType: str,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a view-local constraint."""
        raise NotImplementedError

    def updateConstraint(
        self,
        library: str,
        cell: str,
        view: str,
        constraint: str,
        properties: dict[str, Any],
    ) -> None:
        """Update a view-local constraint."""
        raise NotImplementedError

    def deleteConstraint(
        self,
        library: str,
        cell: str,
        view: str,
        constraint: str,
    ) -> None:
        """Delete a view-local constraint."""
        raise NotImplementedError

    def readToolViews(
        self,
        library: str,
        cell: str,
        view: str,
    ) -> list[dict[str, Any]]:
        """Read toolViews from a view."""
        raise NotImplementedError

    def readToolView(
        self,
        library: str,
        cell: str,
        view: str,
        tool: str,
    ) -> dict[str, Any]:
        """Read one toolView by tool name."""
        raise NotImplementedError

    def createToolView(
        self,
        library: str,
        cell: str,
        view: str,
        tool: str,
        format: str,
        path: str,
        role: str = "derived",
    ) -> dict[str, Any]:
        """Create a toolView entry in view.db."""
        raise NotImplementedError

    def updateToolView(
        self,
        library: str,
        cell: str,
        view: str,
        tool: str,
        properties: dict[str, Any],
    ) -> None:
        """Update a toolView entry."""
        raise NotImplementedError

    def deleteToolView(self, library: str, cell: str, view: str, tool: str) -> None:
        """Delete a toolView entry."""
        raise NotImplementedError

    def readTop(self) -> dict[str, Any]:
        """Read top cell/view reference."""
        raise NotImplementedError

    def setTop(self, library: str, cell: str, view: str = "schematic") -> None:
        """Set top cell/view reference."""
        raise NotImplementedError

    def readTopCell(self) -> Any:
        """Read top cell handle."""
        raise NotImplementedError

    def readTopView(self) -> Any:
        """Read top view handle."""
        raise NotImplementedError

    def findCell(self, cell: str) -> list[tuple[str, str]]:
        """Find cells by exact cell name across libraries."""
        raise NotImplementedError

    def findCells(
        self,
        pattern: str | None = None,
        cellType: str | None = None,
    ) -> list[tuple[str, str]]:
        """Find cells by pattern and optional cell type."""
        raise NotImplementedError

    def findViews(self, viewType: str | None = None) -> list[tuple[str, str, str]]:
        """Find views by optional view type."""
        raise NotImplementedError

    def findInstances(
        self,
        refLibrary: str | None = None,
        refCell: str | None = None,
    ) -> list[dict[str, Any]]:
        """Find CellInstance objects."""
        raise NotImplementedError

    def findComponents(
        self,
        componentDefinitionId: str | None = None,
        refDesignator: str | None = None,
    ) -> list[dict[str, Any]]:
        """Find ComponentInstance objects."""
        raise NotImplementedError

    def findNets(self, name: str | None = None) -> list[dict[str, Any]]:
        """Find nets across schematic/layout views."""
        raise NotImplementedError

    def validateReferences(self) -> Any:
        """Validate references across design.openPCBDB."""
        raise NotImplementedError

    def validateCell(self, library: str, cell: str) -> Any:
        """Validate one cell."""
        raise NotImplementedError

    def validateView(self, library: str, cell: str, view: str) -> Any:
        """Validate one view."""
        raise NotImplementedError

    def validateSymbolContract(self, library: str, cell: str) -> Any:
        """Validate symbol/view.db against schematic/view.db."""
        raise NotImplementedError

    def validateSchematic(self, library: str, cell: str) -> Any:
        """Validate schematic/view.db."""
        raise NotImplementedError

    def validateLayout(self, library: str, cell: str) -> Any:
        """Validate layout/view.db."""
        raise NotImplementedError

    def validateRequirementsCoverage(self) -> Any:
        """Validate requirements coverage across the design database."""
        raise NotImplementedError

    def importToolView(self, library: str, cell: str, view: str, tool: str, path: str) -> Any:
        """Import a tool view into OpenPCBDB semantic data."""
        raise NotImplementedError

    def exportToolView(
        self,
        library: str,
        cell: str,
        view: str,
        tool: str,
        outputPath: str | Path,
    ) -> Any:
        """Export OpenPCBDB semantic data to a tool view."""
        raise NotImplementedError

    def exportKiCad(self, library: str, cell: str, outputPath: str | Path) -> Any:
        """Export a cell to KiCad artifacts."""
        raise NotImplementedError

    def importKiCad(self, path: str | Path, library: str) -> Any:
        """Import KiCad artifacts into a library."""
        raise NotImplementedError

    def exportAltium(self, library: str, cell: str, outputPath: str | Path) -> Any:
        """Export a cell to Altium artifacts."""
        raise NotImplementedError

    def importAltium(self, path: str | Path, library: str) -> Any:
        """Import Altium artifacts into a library."""
        raise NotImplementedError

    def exportConceptHDL(self, library: str, cell: str, outputPath: str | Path) -> Any:
        """Export a cell to ConceptHDL artifacts."""
        raise NotImplementedError

    def importConceptHDL(self, path: str | Path, library: str) -> Any:
        """Import ConceptHDL artifacts into a library."""
        raise NotImplementedError
