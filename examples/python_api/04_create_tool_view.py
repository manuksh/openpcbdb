"""Draft example: attach EDA tool-specific view representations."""

from openpcbdb import OpenPCBDB


db = OpenPCBDB.open("../hierarchical_cell_library")

db.createToolView(
    libName="lib_1",
    cellName="buck_3v3",
    viewName="schematic",
    tool="kicad",
    format="kicad_sch",
    path="toolViews/kicad/view.kicad_sch",
    role="derived",
)

db.createToolView(
    libName="lib_1",
    cellName="buck_3v3",
    viewName="layout",
    tool="altium_designer",
    format="pcbdoc",
    path="toolViews/altium/view.PcbDoc",
    role="snapshot",
)

db.save()
