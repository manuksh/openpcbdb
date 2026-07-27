# OpenPCBDB Python API

OpenPCBDB Python API is an EDA-style interface for reading and writing an
OpenPCBDB design database.

The API follows the same database shape as Virtuoso/OpenAccess-style systems:

```text
design.openPCBDB
libName/
  library.db
  technology.db
  cellName/
    cell.db
    symbol/view.db
    schematic/view.db
    layout/view.db
```

The public API should use EDA naming:

- `OpenPCBDB` is the design database handle.
- `Lib` represents a library.
- `Cell` represents a cell.
- `View` represents one cell view.
- Read APIs use `read*`, for example `readCell`, `readSchematicView`,
  `readDesignContext`.
- Public Python API names use `camelBack`, matching common EDA scripting style.

## Quick example

```python
from openpcbdb import OpenPCBDB

db = OpenPCBDB.open("examples/hierarchical_cell_library")

top = db.readTop()
schematic = db.readSchematicView("lib_1", "power_system")
context = db.readDesignContext()

print(top)
print(schematic.readNets())
print(context["design"]["name"])
```

## Build documentation locally

Install documentation dependencies:

```bash
python -m pip install -e ".[docs]"
```

Serve docs locally:

```bash
mkdocs serve
```

Build static documentation:

```bash
mkdocs build
```
