# Python API Examples

This directory contains draft examples for the future OpenPCBDB Python API.

The examples are written from the point of view of an EDA design engineer:

```text
design database -> lib -> cell -> view -> toolView
```

The API should open `design.openPCBDB` or a directory containing it. The design file is the database index and contains paths to the libraries, technologies, cells, and views.

## Planned Examples

```text
examples/python_api/
  README.md
  01_open_design.py
  02_read_context.py
  03_create_cell.py
  04_create_tool_view.py
```

## API Style

All public API functions use EDA-style `camelBack` naming:

```python
from openpcbdb import OpenPCBDB

db = OpenPCBDB.open("../hierarchical_cell_library")

cell = db.readCell("lib_1", "buck_3v3")
props = db.readCellProperties("lib_1", "buck_3v3")
schematic = db.readView("lib_1", "buck_3v3", "schematic")
```

For AI agents, object-by-object reading may be too slow. The API should also provide bulk context methods:

```python
ctx = db.readCellContext(
    libName="lib_1",
    cellName="power_system",
    depth=1,
    include=["symbol", "schematic", "instances", "nets", "constraints"]
)
```

These context APIs should return compact semantic snapshots suitable for AI reasoning.

