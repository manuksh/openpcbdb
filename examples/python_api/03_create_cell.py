"""Draft example: create a new cell and views."""

from openpcbdb import OpenPCBDB


db = OpenPCBDB.open("../hierarchical_cell_library")

cell = db.createCell(
    libName="lib_1",
    cellName="amplifier",
    cellType="leaf",
    name="Analog Amplifier",
)

db.createView("lib_1", "amplifier", "symbol")
db.createView("lib_1", "amplifier", "schematic")
db.createView("lib_1", "amplifier", "layout")

db.setTop("lib_1", "amplifier", viewName="schematic")
db.save()

