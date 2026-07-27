"""Draft example: open an OpenPCBDB design database.

This file describes the intended API shape. Some calls may not be implemented yet.
"""

from openpcbdb import OpenPCBDB


db = OpenPCBDB.open("../hierarchical_cell_library")

print(db.readDesignName())
print(db.readLibraries())

cell = db.readCell("lib_1", "buck_3v3")
print(cell.readProperties())

schematic = db.readView("lib_1", "buck_3v3", "schematic")
print(schematic.readProperties())

report = db.validate()
report.raiseIfBlocking()

