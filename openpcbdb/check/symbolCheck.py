from __future__ import annotations

from typing import Any

from openpcbdb.model import ValidationReport


def checkSymbol(db: Any, libName: str, cellName: str) -> ValidationReport:
    """Check symbol/view.db port contract."""
    report = ValidationReport()
    try:
        symbol = db.readSymbolView(libName, cellName)
    except Exception as exc:
        report.add("error", f"Cannot read symbol view for {libName}/{cellName}: {exc}", db.path)
        return report

    ports = symbol.readPorts()
    seen: set[str] = set()
    for port in ports:
        portId = port.get("id")
        if not isinstance(portId, str) or not portId:
            report.add("error", f"Symbol port without id in {libName}/{cellName}", symbol.path)
            continue
        if portId in seen:
            report.add("error", f"Duplicate symbol port {portId} in {libName}/{cellName}", symbol.path)
        seen.add(portId)
        if not isinstance(port.get("direction"), str):
            report.add("error", f"Symbol port {portId} has no direction", symbol.path)
        if not isinstance(port.get("electricalType"), str):
            report.add("error", f"Symbol port {portId} has no electricalType", symbol.path)

    interfaces = symbol.data.get("interfaces", [])
    if isinstance(interfaces, list):
        for interface in interfaces:
            if not isinstance(interface, dict):
                continue
            for portId in interface.get("ports", []):
                if portId not in seen:
                    report.add(
                        "error",
                        f"Interface {interface.get('id')} references missing port {portId}",
                        symbol.path,
                    )
    return report
