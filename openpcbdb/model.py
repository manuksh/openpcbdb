from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .errors import ReferenceError, ValidationError
from .io import loadJsonFile, saveJsonFile


DESIGN_MANIFEST_NAMES = ("design.openPCBDB", "design.openpcbdb", "project.openpcbdb")
SUPPORTED_PROJECT_TYPES = {"Project"}
SUPPORTED_LIBRARY_TYPES = {"Library"}
SUPPORTED_CELL_TYPES = {"Cell"}
SUPPORTED_VIEW_TYPES = {"CellSymbol", "Schematic", "PCBLayout"}


@dataclass(frozen=True)
class ValidationResult:
    severity: str
    message: str
    path: Path | None = None

    @property
    def is_error(self) -> bool:
        return self.severity == "error"


@dataclass
class ValidationReport:
    results: list[ValidationResult] = field(default_factory=list)

    def add(self, severity: str, message: str, path: Path | None = None) -> None:
        self.results.append(ValidationResult(severity=severity, message=message, path=path))

    @property
    def errors(self) -> list[ValidationResult]:
        return [result for result in self.results if result.is_error]

    @property
    def warnings(self) -> list[ValidationResult]:
        return [result for result in self.results if result.severity == "warning"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def extend(self, other: "ValidationReport") -> None:
        self.results.extend(other.results)

    def raise_if_blocking(self) -> None:
        if self.errors:
            messages = "\n".join(result.message for result in self.errors)
            raise ValidationError(messages)

    def raiseIfBlocking(self) -> None:
        """Raise when the report has blocking errors."""
        self.raise_if_blocking()

    def summary(self) -> dict[str, int]:
        """Return a compact report summary."""
        return {
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "results": len(self.results),
        }


@dataclass
class View:
    cell: "Cell"
    name: str
    path: Path
    data: dict[str, Any]

    @classmethod
    def load(cls, cell: "Cell", name: str, path: Path) -> "View":
        return cls(cell=cell, name=name, path=path, data=loadJsonFile(path))

    @property
    def type(self) -> str | None:
        value = self.data.get("type")
        return value if isinstance(value, str) else None

    @property
    def constraints(self) -> list[dict[str, Any]]:
        constraints = self.data.get("constraints", [])
        return constraints if isinstance(constraints, list) else []

    @property
    def tool_views(self) -> list[dict[str, Any]]:
        tool_views = self.data.get("toolViews", [])
        return tool_views if isinstance(tool_views, list) else []

    def add_tool_view(self, *, tool: str, format: str, path: str, role: str) -> None:
        tool_views = list(self.tool_views)
        tool_views.append(
            {
                "tool": tool,
                "format": format,
                "path": path,
                "role": role,
            }
        )
        self.data["toolViews"] = tool_views

    def save(self) -> None:
        saveJsonFile(self.path, self.data)

    def read_properties(self) -> dict[str, Any]:
        return dict(self.data)

    def validate(self) -> ValidationReport:
        report = ValidationReport()
        if self.type not in SUPPORTED_VIEW_TYPES:
            report.add("warning", f"Unknown view type {self.type!r}", self.path)
        if self.data.get("library") != self.cell.library.name:
            report.add("error", "View library does not match parent cell library", self.path)
        if self.data.get("cell") != self.cell.name:
            report.add("error", "View cell does not match parent cell name", self.path)
        declared_view = self.data.get("view")
        if declared_view is not None and declared_view != self.name:
            report.add("error", "View name does not match parent view directory", self.path)
        self._validate_refs(report)
        return report

    def _validate_refs(self, report: ValidationReport) -> None:
        for ref in _iter_file_refs(self.data):
            target = (self.path.parent / ref).resolve()
            if not target.exists():
                report.add("error", f"Missing referenced file: {ref}", self.path)


@dataclass
class Cell:
    library: "Library"
    name: str
    path: Path
    data: dict[str, Any]

    @classmethod
    def load(cls, library: "Library", path: Path) -> "Cell":
        data = loadJsonFile(path)
        name = data.get("cell")
        if not isinstance(name, str) or not name:
            raise ReferenceError(f"Cell file has no cell name: {path}")
        return cls(library=library, name=name, path=path, data=data)

    @property
    def views(self) -> dict[str, dict[str, Any]]:
        views = self.data.get("views", {})
        return views if isinstance(views, dict) else {}

    def view(self, name: str) -> View:
        view_ref = self.views.get(name)
        if not isinstance(view_ref, dict):
            raise ReferenceError(f"Cell {self.library.name}/{self.name} has no view {name!r}")
        path_value = view_ref.get("path")
        if not isinstance(path_value, str):
            raise ReferenceError(f"Cell {self.library.name}/{self.name} view {name!r} has no path")
        return View.load(self, name, (self.path.parent / path_value).resolve())

    def read_properties(self) -> dict[str, Any]:
        return dict(self.data)

    def create_view(
        self,
        name: str,
        *,
        view_type: str | None = None,
        properties: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> View:
        if name in self.views and not overwrite:
            raise ReferenceError(f"Cell {self.library.name}/{self.name} already has view {name!r}")

        resolved_type = view_type or _default_view_type(name)
        view_dir = self.path.parent / name
        view_path = view_dir / "view.db"
        if view_path.exists() and not overwrite:
            raise ReferenceError(f"View file already exists: {view_path}")

        data: dict[str, Any] = {
            "openpcbdbVersion": self.data.get("openpcbdbVersion", "0.2.0"),
            "type": resolved_type,
            "library": self.library.name,
            "cell": self.name,
            "view": name,
            "version": self.data.get("version", "0.1.0"),
        }
        if properties:
            data.update(properties)

        saveJsonFile(view_path, data)

        views = dict(self.views)
        views[name] = {
            "path": f"{name}/view.db",
            "type": resolved_type,
            "version": data.get("version", "0.1.0"),
        }
        self.data["views"] = views
        self.save()
        self.library.workspace._index_view(
            self.library.name,
            self.name,
            name,
            {
                "path": str(view_path.resolve().relative_to(self.library.workspace.root)),
                "type": resolved_type,
                "version": data.get("version", "0.1.0"),
            },
        )
        self.library.workspace.save()
        return View.load(self, name, view_path.resolve())

    def save(self) -> None:
        saveJsonFile(self.path, self.data)

    def validate(self) -> ValidationReport:
        report = ValidationReport()
        if self.data.get("type") not in SUPPORTED_CELL_TYPES:
            report.add("error", "Cell file type must be 'Cell'", self.path)
        if self.data.get("library") != self.library.name:
            report.add("error", "Cell library does not match parent library", self.path)
        if self.data.get("cell") != self.name:
            report.add("error", "Cell name mismatch", self.path)
        if not self.views:
            report.add("warning", "Cell has no declared views", self.path)
        self._validate_refs(report)
        for view_name in self.views:
            try:
                report.extend(self.view(view_name).validate())
            except (OSError, ValueError, ReferenceError) as exc:
                report.add("error", f"Could not load view {view_name!r}: {exc}", self.path)
        return report

    def _validate_refs(self, report: ValidationReport) -> None:
        for ref in _iter_file_refs(self.data):
            target = (self.path.parent / ref).resolve()
            if not target.exists():
                report.add("error", f"Missing referenced file: {ref}", self.path)


@dataclass
class Library:
    workspace: "Workspace"
    name: str
    path: Path
    data: dict[str, Any]

    @classmethod
    def load(cls, workspace: "Workspace", name: str, path: Path) -> "Library":
        return cls(workspace=workspace, name=name, path=path, data=loadJsonFile(path))

    @property
    def cells(self) -> list[dict[str, Any]]:
        cells = self.data.get("cells", [])
        return cells if isinstance(cells, list) else []

    def cell(self, name: str) -> Cell:
        for cell_ref in self.cells:
            if cell_ref.get("cell") == name:
                path_value = cell_ref.get("path")
                if not isinstance(path_value, str):
                    raise ReferenceError(f"Library {self.name} cell {name!r} has no path")
                return Cell.load(self, (self.path.parent / path_value).resolve())
        raise ReferenceError(f"Library {self.name} has no cell {name!r}")

    def read_cell(self, name: str) -> Cell:
        return self.cell(name)

    def read_cell_properties(self, name: str) -> dict[str, Any]:
        return self.cell(name).read_properties()

    def create_cell(
        self,
        name: str,
        *,
        cell_type: str = "leaf",
        display_name: str | None = None,
        properties: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> Cell:
        existing_names = {ref.get("cell") for ref in self.cells}
        if name in existing_names and not overwrite:
            raise ReferenceError(f"Library {self.name} already has cell {name!r}")

        cell_dir = self.path.parent / name
        cell_path = cell_dir / "cell.db"
        if cell_path.exists() and not overwrite:
            raise ReferenceError(f"Cell file already exists: {cell_path}")

        data: dict[str, Any] = {
            "openpcbdbVersion": self.data.get("openpcbdbVersion", "0.2.0"),
            "type": "Cell",
            "library": self.name,
            "cell": name,
            "id": f"CELL_{name.upper()}",
            "name": display_name or name,
            "cellType": cell_type,
            "version": "0.1.0",
            "technologyRef": self.data.get("technologyRef"),
            "views": {},
        }
        if properties:
            data.update(properties)

        saveJsonFile(cell_path, data)

        cells = [ref for ref in self.cells if ref.get("cell") != name]
        cells.append({"cell": name, "path": f"{name}/cell.db", "version": data["version"]})
        self.data["cells"] = cells
        self.save()
        self.workspace._index_cell(
            self.name,
            {
                "cell": name,
                "path": str(cell_path.resolve().relative_to(self.workspace.root)),
                "version": data["version"],
                "views": {},
            },
        )
        self.workspace.save()
        return Cell.load(self, cell_path.resolve())

    def save(self) -> None:
        saveJsonFile(self.path, self.data)

    def technology(self) -> dict[str, Any]:
        ref = self.data.get("technologyRef")
        if not isinstance(ref, dict) or not isinstance(ref.get("file"), str):
            raise ReferenceError(f"Library {self.name} has no technologyRef.file")
        return loadJsonFile((self.path.parent / ref["file"]).resolve())

    def validate(self) -> ValidationReport:
        report = ValidationReport()
        if self.data.get("type") not in SUPPORTED_LIBRARY_TYPES:
            report.add("error", "Library file type must be 'Library'", self.path)
        if self.data.get("name") != self.name:
            report.add("error", "Library name does not match project library reference", self.path)
        self._validate_refs(report)
        for cell_ref in self.cells:
            cell_name = cell_ref.get("cell")
            if isinstance(cell_name, str):
                try:
                    report.extend(self.cell(cell_name).validate())
                except (OSError, ValueError, ReferenceError) as exc:
                    report.add("error", f"Could not load cell {cell_name!r}: {exc}", self.path)
        return report

    def _validate_refs(self, report: ValidationReport) -> None:
        for ref in _iter_file_refs(self.data):
            target = (self.path.parent / ref).resolve()
            if not target.exists():
                report.add("error", f"Missing referenced file: {ref}", self.path)


@dataclass
class Workspace:
    path: Path
    data: dict[str, Any]

    @classmethod
    def open(cls, path: str | Path) -> "Workspace":
        project_path = _resolve_design_manifest(Path(path))
        return cls(path=project_path, data=loadJsonFile(project_path))

    @property
    def root(self) -> Path:
        return self.path.parent

    @property
    def libraries(self) -> list[dict[str, Any]]:
        libraries = self.data.get("libraries", [])
        return libraries if isinstance(libraries, list) else []

    def read_design_index(self) -> dict[str, Any]:
        return dict(self.data)

    def requirements(self) -> dict[str, Any]:
        ref = self.data.get("requirementsRef")
        if not isinstance(ref, dict) or not isinstance(ref.get("file"), str):
            raise ReferenceError("Project has no requirementsRef.file")
        return loadJsonFile((self.root / ref["file"]).resolve())

    def library(self, name: str) -> Library:
        for lib_ref in self.libraries:
            if lib_ref.get("name") == name:
                path_value = lib_ref.get("path")
                if not isinstance(path_value, str):
                    raise ReferenceError(f"Library {name!r} has no path")
                return Library.load(self, name, (self.root / path_value).resolve())
        raise ReferenceError(f"Project has no library {name!r}")

    def library_index(self, name: str) -> dict[str, Any]:
        for lib_ref in self.libraries:
            if lib_ref.get("name") == name:
                return lib_ref
        raise ReferenceError(f"Project index has no library {name!r}")

    def cell_index(self, library: str, cell: str) -> dict[str, Any]:
        lib_ref = self.library_index(library)
        cells = lib_ref.get("cells", [])
        if isinstance(cells, list):
            for cell_ref in cells:
                if cell_ref.get("cell") == cell:
                    return cell_ref
        raise ReferenceError(f"Project index has no cell {library}/{cell}")

    def view_index(self, library: str, cell: str, view: str) -> dict[str, Any]:
        cell_ref = self.cell_index(library, cell)
        views = cell_ref.get("views", {})
        if isinstance(views, dict) and isinstance(views.get(view), dict):
            return views[view]
        raise ReferenceError(f"Project index has no view {library}/{cell}/{view}")

    def read_library(self, name: str) -> Library:
        return self.library(name)

    def read_cell(self, library: str, cell: str) -> Cell:
        return self.library(library).cell(cell)

    def read_cell_properties(self, library: str, cell: str) -> dict[str, Any]:
        return self.read_cell(library, cell).read_properties()

    def read_view(self, library: str, cell: str, view: str) -> View:
        return self.read_cell(library, cell).view(view)

    def read_view_properties(self, library: str, cell: str, view: str) -> dict[str, Any]:
        return self.read_view(library, cell, view).read_properties()

    def create_library(
        self,
        name: str,
        *,
        technology_id: str | None = None,
        properties: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> Library:
        existing_names = {ref.get("name") for ref in self.libraries}
        if name in existing_names and not overwrite:
            raise ReferenceError(f"Workspace already has library {name!r}")

        library_dir = self.root / name
        library_path = library_dir / "library.db"
        if library_path.exists() and not overwrite:
            raise ReferenceError(f"Library file already exists: {library_path}")

        tech_id = technology_id or f"TECH_{name.upper()}"
        data: dict[str, Any] = {
            "openpcbdbVersion": self.data.get("openpcbdbVersion", "0.2.0"),
            "type": "Library",
            "name": name,
            "version": "0.1.0",
            "technologyRef": {
                "file": "technology.db",
                "id": tech_id,
                "version": "0.1.0",
            },
            "cells": [],
        }
        if properties:
            data.update(properties)

        saveJsonFile(library_path, data)
        technology_path = library_dir / "technology.db"
        if not technology_path.exists():
            saveJsonFile(
                technology_path,
                {
                    "openpcbdbVersion": data["openpcbdbVersion"],
                    "type": "Technology",
                    "library": name,
                    "id": tech_id,
                    "name": f"{name} Technology",
                    "version": "0.1.0",
                    "fab": {},
                    "designRules": {},
                },
            )

        libraries = [ref for ref in self.libraries if ref.get("name") != name]
        libraries.append(
            {
                "name": name,
                "path": f"{name}/library.db",
                "technology": {
                    "id": tech_id,
                    "path": f"{name}/technology.db",
                    "version": "0.1.0",
                },
                "cells": [],
            }
        )
        self.data["libraries"] = libraries
        self.save()
        return Library.load(self, name, library_path.resolve())

    def create_cell(
        self,
        library: str,
        cell: str,
        *,
        cell_type: str = "leaf",
        display_name: str | None = None,
        properties: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> Cell:
        return self.library(library).create_cell(
            cell,
            cell_type=cell_type,
            display_name=display_name,
            properties=properties,
            overwrite=overwrite,
        )

    def save(self) -> None:
        saveJsonFile(self.path, self.data)

    def _index_cell(self, library: str, cell_ref: dict[str, Any]) -> None:
        libraries = list(self.libraries)
        for lib_ref in libraries:
            if lib_ref.get("name") == library:
                cells = lib_ref.get("cells", [])
                if not isinstance(cells, list):
                    cells = []
                cells = [item for item in cells if item.get("cell") != cell_ref.get("cell")]
                cells.append(cell_ref)
                lib_ref["cells"] = cells
                self.data["libraries"] = libraries
                return
        raise ReferenceError(f"Project index has no library {library!r}")

    def _index_view(
        self,
        library: str,
        cell: str,
        view: str,
        view_ref: dict[str, Any],
    ) -> None:
        libraries = list(self.libraries)
        for lib_ref in libraries:
            if lib_ref.get("name") != library:
                continue
            cells = lib_ref.get("cells", [])
            if not isinstance(cells, list):
                cells = []
            for cell_ref in cells:
                if cell_ref.get("cell") == cell:
                    views = cell_ref.get("views", {})
                    if not isinstance(views, dict):
                        views = {}
                    views[view] = view_ref
                    cell_ref["views"] = views
                    self.data["libraries"] = libraries
                    return
        raise ReferenceError(f"Project index has no cell {library}/{cell}")

    def top_cell(self) -> Cell:
        top = self.data.get("top")
        if not isinstance(top, dict):
            raise ReferenceError("Project has no top cell")
        library_name = top.get("library")
        cell_name = top.get("cell")
        if not isinstance(library_name, str) or not isinstance(cell_name, str):
            raise ReferenceError("Project top must include library and cell")
        return self.library(library_name).cell(cell_name)

    def top_view(self) -> View:
        top = self.data.get("top")
        if not isinstance(top, dict) or not isinstance(top.get("view"), str):
            raise ReferenceError("Project top must include view")
        return self.top_cell().view(top["view"])

    def validate(self) -> ValidationReport:
        report = ValidationReport()
        if self.data.get("type") not in SUPPORTED_PROJECT_TYPES:
            report.add("error", "Project file type must be 'Project'", self.path)
        self._validate_refs(report)
        try:
            self.requirements()
        except (OSError, ValueError, ReferenceError) as exc:
            report.add("error", f"Could not load requirements: {exc}", self.path)
        for lib_ref in self.libraries:
            name = lib_ref.get("name")
            if isinstance(name, str):
                try:
                    report.extend(self.library(name).validate())
                except (OSError, ValueError, ReferenceError) as exc:
                    report.add("error", f"Could not load library {name!r}: {exc}", self.path)
        try:
            self.top_view()
        except (OSError, ValueError, ReferenceError) as exc:
            report.add("error", f"Could not load top view: {exc}", self.path)
        return report

    def _validate_refs(self, report: ValidationReport) -> None:
        for ref in _iter_file_refs(self.data):
            target = (self.root / ref).resolve()
            if not target.exists():
                report.add("error", f"Missing referenced file: {ref}", self.path)


def _iter_file_refs(data: Any) -> Iterable[str]:
    if isinstance(data, dict):
        for key, value in data.items():
            if key in {"file", "path", "cellRef"} and isinstance(value, str):
                yield value
            elif key == "viewBinding" and isinstance(value, dict):
                for view_ref in value.values():
                    if isinstance(view_ref, str):
                        yield view_ref
            elif isinstance(value, (dict, list)):
                yield from _iter_file_refs(value)
    elif isinstance(data, list):
        for item in data:
            yield from _iter_file_refs(item)


def _resolve_design_manifest(path: Path) -> Path:
    resolved = path.resolve()
    if resolved.is_dir():
        for manifest_name in DESIGN_MANIFEST_NAMES:
            candidate = resolved / manifest_name
            if candidate.exists():
                return candidate.resolve()
        raise ReferenceError(
            f"No design manifest found in {resolved}; expected one of {DESIGN_MANIFEST_NAMES}"
        )
    return resolved


def _default_view_type(name: str) -> str:
    if name == "symbol":
        return "CellSymbol"
    if name == "schematic":
        return "Schematic"
    if name == "layout":
        return "PCBLayout"
    return "View"
