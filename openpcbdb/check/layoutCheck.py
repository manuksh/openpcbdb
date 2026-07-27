from __future__ import annotations

from typing import Any

from openpcbdb.model import ValidationReport


def checkLayout(db: Any, libName: str, cellName: str) -> ValidationReport:
    """Check layout/view.db against schematic and technology basics."""
    report = ValidationReport()
    try:
        layout = db.readLayoutView(libName, cellName)
    except Exception as exc:
        report.add("error", f"Cannot read layout view for {libName}/{cellName}: {exc}", db.path)
        return report

    techLayers = _techLayers(db, libName, layout.data.get("technologyRef"), report)
    schematicObjects = _schematicObjects(db, libName, cellName)
    for placement in layout.readPlacements():
        target = placement.get("instance") or placement.get("refDesignator")
        if target and schematicObjects and target not in schematicObjects:
            report.add("warning", f"Placement references object not found in schematic: {target}", layout.path)

    for route in layout.readRoutes():
        if not isinstance(route, dict):
            continue
        layer = route.get("layer")
        if layer and techLayers and layer not in techLayers:
            report.add("error", f"Route references unknown technology layer {layer}", layout.path)

    for zone in layout.readZones():
        if not isinstance(zone, dict):
            continue
        layer = zone.get("layer")
        if layer and techLayers and layer not in techLayers:
            report.add("error", f"Zone references unknown technology layer {layer}", layout.path)

    if "constraints" in layout.data and not isinstance(layout.data["constraints"], list):
        report.add("error", "Layout constraints must be a list", layout.path)
    return report


def _techLayers(db: Any, libName: str, technologyRef: Any, report: ValidationReport) -> set[str]:
    try:
        tech = db.readLib(libName).readTech()
        data = tech.readProperties()
    except Exception as exc:
        report.add("error", f"Cannot read technology for layout {libName}: {exc}", db.path)
        return set()
    if isinstance(technologyRef, dict):
        expectedId = technologyRef.get("id")
        if expectedId and data.get("id") != expectedId:
            report.add("error", f"Layout technologyRef id {expectedId} does not match library technology", tech.path)
    layers = data.get("stackup", {}).get("layers", [])
    if not isinstance(layers, list):
        return set()
    return {layer["id"] for layer in layers if isinstance(layer, dict) and isinstance(layer.get("id"), str)}


def _schematicObjects(db: Any, libName: str, cellName: str) -> set[str]:
    try:
        schematic = db.readSchematicView(libName, cellName)
    except Exception:
        return set()
    names: set[str] = set()
    for inst in schematic.data.get("instances", []):
        if isinstance(inst, dict) and isinstance(inst.get("id"), str):
            names.add(inst["id"])
    for comp in schematic.data.get("components", []):
        if isinstance(comp, dict) and isinstance(comp.get("refDesignator"), str):
            names.add(comp["refDesignator"])
    return names
