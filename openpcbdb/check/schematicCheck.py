from __future__ import annotations

from typing import Any

from openpcbdb.model import ValidationReport


def checkSchematic(db: Any, libName: str, cellName: str) -> ValidationReport:
    """Check schematic/view.db connectivity and instance references."""
    report = ValidationReport()
    try:
        schematic = db.readSchematicView(libName, cellName)
    except Exception as exc:
        report.add("error", f"Cannot read schematic view for {libName}/{cellName}: {exc}", db.path)
        return report

    symbolPorts = _symbolPorts(db, libName, cellName, report)
    for externalPort in schematic.data.get("externalPorts", []):
        if not isinstance(externalPort, dict):
            continue
        portId = externalPort.get("symbolPort")
        if portId not in symbolPorts:
            report.add("error", f"External port references missing symbol port {portId}", schematic.path)

    instPorts: dict[str, set[str]] = {"self": symbolPorts}
    for inst in schematic.data.get("instances", []):
        if not isinstance(inst, dict):
            continue
        instName = inst.get("id")
        if not isinstance(instName, str):
            report.add("error", "CellInstance without id", schematic.path)
            continue
        if inst.get("type") != "CellInstance":
            continue
        childLib = inst.get("library")
        childCell = inst.get("cell")
        if not isinstance(childLib, str) or not isinstance(childCell, str):
            report.add("error", f"CellInstance {instName} missing library/cell", schematic.path)
            continue
        try:
            db.readCell(childLib, childCell)
            instPorts[instName] = _symbolPorts(db, childLib, childCell, report)
        except Exception as exc:
            report.add("error", f"CellInstance {instName} cannot resolve {childLib}/{childCell}: {exc}", schematic.path)

    for comp in schematic.data.get("components", []):
        if not isinstance(comp, dict):
            continue
        if not comp.get("refDesignator"):
            report.add("error", "ComponentInstance missing refDesignator", schematic.path)
        if not comp.get("componentDefinitionId"):
            report.add("error", f"ComponentInstance {comp.get('refDesignator')} missing componentDefinitionId", schematic.path)

    for net in schematic.readNets():
        netId = net.get("id", net.get("name"))
        connections = net.get("connections", [])
        if not isinstance(connections, list) or not connections:
            report.add("warning", f"Net {netId} has no connections", schematic.path)
            continue
        for conn in connections:
            if not isinstance(conn, dict):
                continue
            if "instance" in conn:
                instName = conn.get("instance")
                portName = conn.get("port")
                if instName not in instPorts:
                    report.add("error", f"Net {netId} references missing instance {instName}", schematic.path)
                elif portName not in instPorts.get(str(instName), set()):
                    report.add("error", f"Net {netId} references missing port {instName}.{portName}", schematic.path)
            elif "externalPort" in conn:
                if conn.get("externalPort") not in symbolPorts:
                    report.add("error", f"Net {netId} references missing externalPort {conn.get('externalPort')}", schematic.path)
            elif "component" in conn:
                if not conn.get("pin"):
                    report.add("error", f"Net {netId} component connection missing pin", schematic.path)
            else:
                report.add("error", f"Net {netId} has unknown connection shape", schematic.path)
    return report


def _symbolPorts(db: Any, libName: str, cellName: str, report: ValidationReport) -> set[str]:
    try:
        return {port["id"] for port in db.readSymbolView(libName, cellName).readPorts() if isinstance(port.get("id"), str)}
    except Exception as exc:
        report.add("error", f"Cannot read symbol ports for {libName}/{cellName}: {exc}", db.path)
        return set()
