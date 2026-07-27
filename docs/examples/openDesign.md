# Open a design database

OpenPCBDB starts from `design.openPCBDB`. You can pass either the design
directory or the manifest file.

```python
from openpcbdb import OpenPCBDB

db = OpenPCBDB.open("examples/hierarchical_cell_library")

print(db.readDesignName())
print(db.readDesignVersion())
print(db.readLibraries())
```

Read the top cell/view:

```python
top = db.readTop()

print(top["library"])
print(top["cell"])
print(top["view"])
```

Read a cell and one of its views:

```python
cell = db.readCell("lib_1", "buck_3v3")
schematic = db.readSchematicView("lib_1", "buck_3v3")

print(cell.readProperties())
print(schematic.readNets())
```
