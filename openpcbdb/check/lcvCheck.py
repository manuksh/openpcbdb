from __future__ import annotations

from pathlib import Path
from typing import Any

from openpcbdb.model import ValidationReport


def checkDesign(db: Any) -> ValidationReport:
    """Run all available design database checks."""
    report = checkLcv(db)
    for libRef in db.readLibraries():
        libName = libRef.get("name")
        if isinstance(libName, str):
            report.extend(checkLib(db, libName))
            from .techCheck import checkTech

            report.extend(checkTech(db, libName))
            cells = libRef.get("cells", [])
            if isinstance(cells, list):
                for cellRef in cells:
                    cellName = cellRef.get("cell")
                    if not isinstance(cellName, str):
                        continue
                    views = cellRef.get("views", {})
                    if not isinstance(views, dict):
                        continue
                    if "symbol" in views:
                        from .symbolCheck import checkSymbol

                        report.extend(checkSymbol(db, libName, cellName))
                    if "schematic" in views:
                        from .schematicCheck import checkSchematic

                        report.extend(checkSchematic(db, libName, cellName))
                    if "layout" in views:
                        from .layoutCheck import checkLayout

                        report.extend(checkLayout(db, libName, cellName))
    top = db.readTop()
    if not top:
        report.add("error", "design.openPCBDB has no top reference", db.path)
    else:
        _checkTop(db, top, report)
    return report


def checkLcv(db: Any) -> ValidationReport:
    """Check design.openPCBDB library/cell/view index."""
    report = ValidationReport()
    data = db.readDesignProperties()
    if data.get("type") != "Project":
        report.add("error", "design.openPCBDB type must be Project", db.path)
    if not data.get("libraries"):
        report.add("warning", "design.openPCBDB has no libraries", db.path)
    for libRef in db.readLibraries():
        _checkRefPath(db.root, libRef, "path", report, db.path)
        techRef = libRef.get("technology")
        if isinstance(techRef, dict):
            _checkRefPath(db.root, techRef, "path", report, db.path)
        cells = libRef.get("cells", [])
        if isinstance(cells, list):
            for cellRef in cells:
                _checkRefPath(db.root, cellRef, "path", report, db.path)
                views = cellRef.get("views", {})
                if isinstance(views, dict):
                    for viewRef in views.values():
                        if isinstance(viewRef, dict):
                            _checkRefPath(db.root, viewRef, "path", report, db.path)
    return report


def checkLib(db: Any, libName: str) -> ValidationReport:
    """Check one library."""
    report = ValidationReport()
    try:
        lib = db.readLib(libName)
    except Exception as exc:
        report.add("error", f"Cannot read library {libName}: {exc}", db.path)
        return report

    if lib.data.get("type") != "Library":
        report.add("error", f"Library {libName} type must be Library", lib.path)
    if lib.data.get("name") != libName:
        report.add("error", f"Library name mismatch for {libName}", lib.path)
    if not lib.readTechnologyRef():
        report.add("warning", f"Library {libName} has no technologyRef", lib.path)
    for cellRef in lib.readCells():
        cellName = cellRef.get("cell")
        if isinstance(cellName, str):
            report.extend(checkCell(db, libName, cellName))
    return report


def checkCell(db: Any, libName: str, cellName: str) -> ValidationReport:
    """Check one cell."""
    report = ValidationReport()
    try:
        cell = db.readCell(libName, cellName)
    except Exception as exc:
        report.add("error", f"Cannot read cell {libName}/{cellName}: {exc}", db.path)
        return report

    if cell.data.get("type") != "Cell":
        report.add("error", f"Cell {libName}/{cellName} type must be Cell", cell.path)
    if cell.data.get("library") != libName:
        report.add("error", f"Cell library mismatch for {libName}/{cellName}", cell.path)
    if cell.data.get("cell") != cellName:
        report.add("error", f"Cell name mismatch for {libName}/{cellName}", cell.path)
    if not cell.readViews():
        report.add("warning", f"Cell {libName}/{cellName} has no views", cell.path)
    for viewName in cell.readViews():
        report.extend(checkView(db, libName, cellName, viewName))
    return report


def checkView(db: Any, libName: str, cellName: str, viewName: str) -> ValidationReport:
    """Check one view."""
    report = ValidationReport()
    try:
        view = db.readView(libName, cellName, viewName)
    except Exception as exc:
        report.add("error", f"Cannot read view {libName}/{cellName}/{viewName}: {exc}", db.path)
        return report

    if view.data.get("library") != libName:
        report.add("error", f"View library mismatch for {libName}/{cellName}/{viewName}", view.path)
    if view.data.get("cell") != cellName:
        report.add("error", f"View cell mismatch for {libName}/{cellName}/{viewName}", view.path)
    declaredView = view.data.get("view")
    if declaredView is not None and declaredView != viewName:
        report.add("error", f"View name mismatch for {libName}/{cellName}/{viewName}", view.path)
    return report


def _checkTop(db: Any, top: dict[str, Any], report: ValidationReport) -> None:
    libName = top.get("library")
    cellName = top.get("cell")
    viewName = top.get("view")
    if not isinstance(libName, str) or not isinstance(cellName, str) or not isinstance(viewName, str):
        report.add("error", "Top reference must include library, cell, and view", db.path)
        return
    report.extend(checkView(db, libName, cellName, viewName))


def _checkRefPath(
    root: Path,
    ref: dict[str, Any],
    key: str,
    report: ValidationReport,
    ownerPath: Path,
) -> None:
    value = ref.get(key)
    if not isinstance(value, str) or not value:
        report.add("error", f"Missing reference path key {key}", ownerPath)
        return
    if not (root / value).resolve().exists():
        report.add("error", f"Referenced path does not exist: {value}", ownerPath)
