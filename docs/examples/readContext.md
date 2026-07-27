# Read AI context

AI agents should not be forced to open every JSON file manually. Context APIs
provide compact semantic snapshots from the design database.

```python
from openpcbdb import OpenPCBDB

db = OpenPCBDB.open("examples/hierarchical_cell_library")

designContext = db.readDesignContext(depth=1)

print(designContext["design"]["name"])
print(designContext["top"])
print(designContext["libraries"])
```

Read context for one cell:

```python
cellContext = db.readCellContext(
    libName="lib_1",
    cellName="power_system",
    depth=1,
    include=[
        "symbol",
        "schematic",
        "layout",
        "instances",
        "nets",
        "constraints",
        "requirements",
    ],
)

print(cellContext["cell"]["name"])
print(cellContext["views"].keys())
```

This is the preferred path for AI workflows: one semantic read gives the agent
enough design intent to reason before making edits.
