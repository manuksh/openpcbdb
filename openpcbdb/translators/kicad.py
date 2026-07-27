from __future__ import annotations

from pathlib import Path
from typing import Any


def readKiCadToolView(view: Any) -> dict[str, Any]:
    """Read the KiCad toolView entry from an OpenPCBDB view."""
    return view.readToolView("kicad")


def createKiCadToolView(
    view: Any,
    path: str | Path,
    format: str,
    role: str = "derived",
    properties: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a KiCad toolView entry on an OpenPCBDB view."""
    return view.createToolView(
        tool="kicad",
        format=format,
        path=str(path),
        role=role,
        properties=properties,
    )


def importKiCadSchematic(
    db: Any,
    libName: str,
    cellName: str,
    path: str | Path,
    properties: dict[str, Any] | None = None,
) -> Any:
    """Import a KiCad schematic into schematic/view.db."""
    raise NotImplementedError("KiCad schematic import is not implemented yet")


def exportKiCadSchematic(
    db: Any,
    libName: str,
    cellName: str,
    path: str | Path,
    properties: dict[str, Any] | None = None,
) -> Path:
    """Export schematic/view.db to a KiCad schematic file."""
    raise NotImplementedError("KiCad schematic export is not implemented yet")


def importKiCadLayout(
    db: Any,
    libName: str,
    cellName: str,
    path: str | Path,
    properties: dict[str, Any] | None = None,
) -> Any:
    """Import a KiCad PCB layout into layout/view.db."""
    raise NotImplementedError("KiCad layout import is not implemented yet")


def exportKiCadLayout(
    db: Any,
    libName: str,
    cellName: str,
    path: str | Path,
    properties: dict[str, Any] | None = None,
) -> Path:
    """Export layout/view.db to a KiCad PCB file."""
    raise NotImplementedError("KiCad layout export is not implemented yet")
