from __future__ import annotations

from pathlib import Path
from typing import Any


def readAltiumToolView(view: Any) -> dict[str, Any]:
    """Read the Altium Designer toolView entry from an OpenPCBDB view."""
    return view.readToolView("altium_designer")


def createAltiumToolView(
    view: Any,
    path: str | Path,
    format: str,
    role: str = "snapshot",
    properties: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create an Altium Designer toolView entry on an OpenPCBDB view."""
    return view.createToolView(
        tool="altium_designer",
        format=format,
        path=str(path),
        role=role,
        properties=properties,
    )


def importAltiumSchematic(
    db: Any,
    libName: str,
    cellName: str,
    path: str | Path,
    properties: dict[str, Any] | None = None,
) -> Any:
    """Import an Altium schematic into schematic/view.db."""
    raise NotImplementedError("Altium schematic import is not implemented yet")


def exportAltiumSchematic(
    db: Any,
    libName: str,
    cellName: str,
    path: str | Path,
    properties: dict[str, Any] | None = None,
) -> Path:
    """Export schematic/view.db to an Altium schematic file."""
    raise NotImplementedError("Altium schematic export is not implemented yet")


def importAltiumLayout(
    db: Any,
    libName: str,
    cellName: str,
    path: str | Path,
    properties: dict[str, Any] | None = None,
) -> Any:
    """Import an Altium PCB layout into layout/view.db."""
    raise NotImplementedError("Altium layout import is not implemented yet")


def exportAltiumLayout(
    db: Any,
    libName: str,
    cellName: str,
    path: str | Path,
    properties: dict[str, Any] | None = None,
) -> Path:
    """Export layout/view.db to an Altium PCB file."""
    raise NotImplementedError("Altium layout export is not implemented yet")
