from __future__ import annotations

from pathlib import Path
from typing import Any

from openpcbdb.io import saveJsonFile
from openpcbdb.library import Lib
from openpcbdb.model import Workspace

from .context import DesignContextMixin
from .properties import DesignPropertiesMixin
from .requirements import DesignRequirementsMixin


class OpenPCBDB(
    DesignPropertiesMixin,
    DesignRequirementsMixin,
    DesignContextMixin,
    Workspace,
):
    """OpenPCBDB design database handle.

    This is the public EDA-style database API entry point. It opens
    `design.openPCBDB`, reads the design index, and provides access to
    libraries, cells, views, requirements, and AI context snapshots.
    """

    @classmethod
    def open(cls, path: str | Path) -> "OpenPCBDB":
        """Open design.openPCBDB or a directory containing design.openPCBDB."""
        workspace = Workspace.open(path)
        return cls(path=workspace.path, data=workspace.data)

    @classmethod
    def create(
        cls,
        path: str | Path,
        name: str,
        topCell: tuple[str, str, str] | None = None,
    ) -> "OpenPCBDB":
        """Create a new design.openPCBDB database index."""
        rootPath = Path(path).resolve()
        designPath = rootPath if rootPath.suffix else rootPath / "design.openPCBDB"
        topLib, topCellName, topView = topCell or ("worklib", "top", "schematic")
        data: dict[str, Any] = {
            "openpcbdbVersion": "0.2.0",
            "type": "Project",
            "id": designPath.parent.name,
            "name": name,
            "version": "0.1.0",
            "top": {
                "library": topLib,
                "cell": topCellName,
                "view": topView,
                "path": f"{topLib}/{topCellName}/{topView}/view.db",
            },
            "libraries": [],
        }
        saveJsonFile(designPath, data)
        return cls.open(designPath)

    def close(self) -> None:
        """Close the design database handle.

        JSON storage does not keep an open file handle, so this is currently
        a no-op. Future SQLite/binary stores may release resources here.
        """

    def reload(self) -> None:
        """Reload design.openPCBDB from disk."""
        refreshed = self.open(self.path)
        self.data = refreshed.data

    def readLib(self, libName: str) -> Any:
        """Read a library handle."""
        return self.library(libName)

    def readLibrary(self, libName: str) -> Any:
        """Read a library handle."""
        return self.readLib(libName)

    def readLibraries(self) -> list[dict[str, Any]]:
        """Read library index entries from design.openPCBDB."""
        return list(self.libraries)

    def library(self, name: str) -> Lib:
        """Read a typed library handle."""
        for libRef in self.libraries:
            if libRef.get("name") == name:
                pathValue = libRef.get("path")
                if not isinstance(pathValue, str):
                    from openpcbdb.errors import ReferenceError

                    raise ReferenceError(f"Library {name!r} has no path")
                return Lib.load(self, name, (self.root / pathValue).resolve())
        from openpcbdb.errors import ReferenceError

        raise ReferenceError(f"Project has no library {name!r}")

    def readLibraryProperties(self, libName: str) -> dict[str, Any]:
        """Read library.db properties."""
        return dict(self.readLib(libName).data)

    def readCell(self, libName: str, cellName: str) -> Any:
        """Read a cell handle."""
        return self.library(libName).cell(cellName)

    def readCellProperties(self, libName: str, cellName: str) -> dict[str, Any]:
        """Read cell.db properties."""
        return self.readCell(libName, cellName).read_properties()

    def readView(self, libName: str, cellName: str, viewName: str) -> Any:
        """Read a view handle."""
        return self.readCell(libName, cellName).view(viewName)

    def readViewProperties(self, libName: str, cellName: str, viewName: str) -> dict[str, Any]:
        """Read view.db properties."""
        return self.readView(libName, cellName, viewName).read_properties()

    def readSchematicView(self, libName: str, cellName: str) -> Any:
        """Read schematic/view.db."""
        return self.readView(libName, cellName, "schematic")

    def readLayoutView(self, libName: str, cellName: str) -> Any:
        """Read layout/view.db."""
        return self.readView(libName, cellName, "layout")

    def readSymbolView(self, libName: str, cellName: str) -> Any:
        """Read symbol/view.db."""
        return self.readView(libName, cellName, "symbol")

    def readTop(self) -> dict[str, Any]:
        """Read top cell/view reference."""
        top = self.data.get("top", {})
        return dict(top) if isinstance(top, dict) else {}

    def readTopCell(self) -> Any:
        """Read top cell handle."""
        return self.top_cell()

    def readTopView(self) -> Any:
        """Read top view handle."""
        return self.top_view()

    def checkDesign(self) -> Any:
        """Run all EDA database checks."""
        from openpcbdb.check import checkDesign

        return checkDesign(self)

    def checkLcv(self) -> Any:
        """Run library/cell/view hierarchy checks."""
        from openpcbdb.check import checkLcv

        return checkLcv(self)

    def checkTech(self, libName: str) -> Any:
        """Run technology checks for one library."""
        from openpcbdb.check import checkTech

        return checkTech(self, libName)

    def checkSymbol(self, libName: str, cellName: str) -> Any:
        """Run symbol contract checks for one cell."""
        from openpcbdb.check import checkSymbol

        return checkSymbol(self, libName, cellName)

    def checkSchematic(self, libName: str, cellName: str) -> Any:
        """Run schematic checks for one cell."""
        from openpcbdb.check import checkSchematic

        return checkSchematic(self, libName, cellName)

    def checkLayout(self, libName: str, cellName: str) -> Any:
        """Run layout checks for one cell."""
        from openpcbdb.check import checkLayout

        return checkLayout(self, libName, cellName)

    def validate(self) -> Any:
        """Validate the design database.

        This uses the EDA check layer. The older Workspace validation remains
        available internally as the transitional reference checker.
        """
        return self.checkDesign()

    def createLibrary(
        self,
        libName: str,
        technologyRef: dict[str, Any] | None = None,
        properties: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> Any:
        """Create a library and update design.openPCBDB."""
        techId = None
        if technologyRef:
            techId = technologyRef.get("id")
        return self.create_library(
            libName,
            technology_id=techId,
            properties=properties,
            overwrite=overwrite,
        )

    def createCell(
        self,
        libName: str,
        cellName: str,
        cellType: str = "leaf",
        name: str | None = None,
        properties: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> Any:
        """Create a cell and update library.db/design.openPCBDB."""
        return self.readLib(libName).createCell(
            cellName,
            cellType=cellType,
            name=name,
            properties=properties,
            overwrite=overwrite,
        )

    def createView(
        self,
        libName: str,
        cellName: str,
        viewName: str,
        viewType: str | None = None,
        properties: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> Any:
        """Create a cell view and update cell.db/design.openPCBDB."""
        return self.readCell(libName, cellName).createView(
            viewName,
            viewType=viewType,
            properties=properties,
            overwrite=overwrite,
        )
