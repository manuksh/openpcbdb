"""Draft example: read AI-friendly semantic context.

Context APIs should reduce many small object reads into one compact semantic snapshot.
"""

from openpcbdb import OpenPCBDB


db = OpenPCBDB.open("../hierarchical_cell_library")

designContext = db.readDesignContext(depth=1)
print(designContext)

cellContext = db.readCellContext(
    libName="lib_1",
    cellName="power_system",
    depth=1,
    include=[
        "symbol",
        "schematic",
        "instances",
        "childSymbols",
        "nets",
        "constraints",
        "requirements",
    ],
)
print(cellContext)

