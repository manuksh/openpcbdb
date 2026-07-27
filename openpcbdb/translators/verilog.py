from __future__ import annotations

from pathlib import Path
from typing import Any


def readVerilogToolView(view: Any) -> dict[str, Any]:
    """Read the Verilog toolView entry from an OpenPCBDB view."""
    return view.readToolView("verilog")


def createVerilogToolView(
    view: Any,
    path: str | Path,
    format: str = "verilog",
    role: str = "derived",
    properties: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a Verilog toolView entry on an OpenPCBDB view."""
    return view.createToolView(
        tool="verilog",
        format=format,
        path=str(path),
        role=role,
        properties=properties,
    )


def importVerilogModule(
    db: Any,
    libName: str,
    cellName: str,
    path: str | Path,
    properties: dict[str, Any] | None = None,
) -> Any:
    """Import a Verilog module into verilog/view.db or netlist/view.db."""
    raise NotImplementedError("Verilog module import is not implemented yet")


def exportVerilogModule(
    db: Any,
    libName: str,
    cellName: str,
    path: str | Path,
    sourceViewName: str = "schematic",
    properties: dict[str, Any] | None = None,
) -> Path:
    """Export an OpenPCBDB view to a Verilog module file."""
    raise NotImplementedError("Verilog module export is not implemented yet")
