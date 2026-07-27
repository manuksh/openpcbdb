from __future__ import annotations

from pathlib import Path
from typing import Any

from openpcbdb.cell import Cell
from openpcbdb.errors import ReferenceError
from openpcbdb.io import loadJsonFile, saveJsonFile
from openpcbdb.model import Library as ModelLibrary

from .index import LibraryIndexMixin
from .tech import Tech


class Lib(LibraryIndexMixin, ModelLibrary):
    """EDA library object."""

    @classmethod
    def load(cls, workspace: Any, name: str, path: Path) -> "Lib":
        """Load library.db."""
        return cls(workspace=workspace, name=name, path=path, data=loadJsonFile(path))

    def readCell(self, cellName: str) -> Cell:
        """Read a cell handle from this library."""
        return self.cell(cellName)

    def readCellProperties(self, cellName: str) -> dict[str, Any]:
        """Read cell.db properties."""
        return self.readCell(cellName).readProperties()

    def cell(self, name: str) -> Cell:
        for cellRef in self.cells:
            if cellRef.get("cell") == name:
                pathValue = cellRef.get("path")
                if not isinstance(pathValue, str):
                    raise ReferenceError(f"Library {self.name} cell {name!r} has no path")
                return Cell.load(self, (self.path.parent / pathValue).resolve())
        raise ReferenceError(f"Library {self.name} has no cell {name!r}")

    def createCell(
        self,
        cellName: str,
        cellType: str = "leaf",
        name: str | None = None,
        properties: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> Cell:
        """Create a cell and update library.db/design.openPCBDB."""
        existingNames = {ref.get("cell") for ref in self.cells}
        if cellName in existingNames and not overwrite:
            raise ReferenceError(f"Library {self.name} already has cell {cellName!r}")

        cellDir = self.path.parent / cellName
        cellPath = cellDir / "cell.db"
        if cellPath.exists() and not overwrite:
            raise ReferenceError(f"Cell file already exists: {cellPath}")

        data: dict[str, Any] = {
            "openpcbdbVersion": self.data.get("openpcbdbVersion", "0.2.0"),
            "type": "Cell",
            "library": self.name,
            "cell": cellName,
            "id": f"CELL_{cellName.upper()}",
            "name": name or cellName,
            "cellType": cellType,
            "version": "0.1.0",
            "technologyRef": self.data.get("technologyRef"),
            "views": {},
        }
        if properties:
            data.update(properties)

        saveJsonFile(cellPath, data)
        cells = [ref for ref in self.cells if ref.get("cell") != cellName]
        cells.append({"cell": cellName, "path": f"{cellName}/cell.db", "version": data["version"]})
        self.data["cells"] = cells
        self.save()
        self.workspace._index_cell(
            self.name,
            {
                "cell": cellName,
                "path": str(cellPath.resolve().relative_to(self.workspace.root)),
                "version": data["version"],
                "views": {},
            },
        )
        self.workspace.save()
        return Cell.load(self, cellPath.resolve())

    def readTech(self) -> Tech:
        """Read library technology database."""
        ref = self.data.get("technologyRef")
        if not isinstance(ref, dict) or not isinstance(ref.get("file"), str):
            raise ReferenceError(f"Library {self.name} has no technologyRef.file")
        return Tech.load(self, (self.path.parent / ref["file"]).resolve())

    def readTechnology(self) -> Tech:
        """Read library technology database."""
        return self.readTech()

    def technology(self) -> dict[str, Any]:
        """Read technology.db properties for compatibility."""
        return self.readTech().readProperties()

    def save(self) -> None:
        """Save library.db."""
        saveJsonFile(self.path, self.data)
