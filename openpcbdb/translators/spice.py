from __future__ import annotations

from pathlib import Path
from typing import Any


def readSpiceToolView(view: Any) -> dict[str, Any]:
    """Read the SPICE toolView entry from an OpenPCBDB view."""
    return view.readToolView("spice")


def createSpiceToolView(
    view: Any,
    path: str | Path,
    format: str = "spice",
    role: str = "derived",
    properties: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a SPICE toolView entry on an OpenPCBDB view."""
    return view.createToolView(
        tool="spice",
        format=format,
        path=str(path),
        role=role,
        properties=properties,
    )


def importSpiceNetlist(
    db: Any,
    libName: str,
    cellName: str,
    path: str | Path,
    properties: dict[str, Any] | None = None,
) -> Any:
    """Import a SPICE netlist into spice/view.db or netlist/view.db."""
    raise NotImplementedError("SPICE netlist import is not implemented yet")


def exportSpiceNetlist(
    db: Any,
    libName: str,
    cellName: str,
    path: str | Path,
    sourceViewName: str = "schematic",
    properties: dict[str, Any] | None = None,
) -> Path:
    """Export an OpenPCBDB view to a SPICE netlist."""
    raise NotImplementedError("SPICE netlist export is not implemented yet")
