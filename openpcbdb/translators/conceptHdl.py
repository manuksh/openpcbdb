from __future__ import annotations

from pathlib import Path
from typing import Any


def readConceptHdlToolView(view: Any) -> dict[str, Any]:
    """Read the ConceptHDL toolView entry from an OpenPCBDB view."""
    return view.readToolView("concept_hdl")


def createConceptHdlToolView(
    view: Any,
    path: str | Path,
    format: str = "concept_hdl",
    role: str = "derived",
    properties: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a ConceptHDL toolView entry on a schematic view."""
    return view.createToolView(
        tool="concept_hdl",
        format=format,
        path=str(path),
        role=role,
        properties=properties,
    )


def importConceptHdlSchematic(
    db: Any,
    libName: str,
    cellName: str,
    path: str | Path,
    properties: dict[str, Any] | None = None,
) -> Any:
    """Import a ConceptHDL schematic into schematic/view.db."""
    raise NotImplementedError("ConceptHDL schematic import is not implemented yet")


def exportConceptHdlSchematic(
    db: Any,
    libName: str,
    cellName: str,
    path: str | Path,
    properties: dict[str, Any] | None = None,
) -> Path:
    """Export schematic/view.db to a ConceptHDL schematic representation."""
    raise NotImplementedError("ConceptHDL schematic export is not implemented yet")
