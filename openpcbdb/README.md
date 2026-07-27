# OpenPCBDB Python Package Structure

This package should be organized as an EDA-style database API, not as a generic CRUD wrapper.

The public API should feel familiar to EDA users:

```python
from openpcbdb import OpenPCBDB

db = OpenPCBDB.open("design.openPCBDB")
lib = db.readLib("lib_1")
cell = db.readCell("lib_1", "buck_3v3")
view = db.readView("lib_1", "buck_3v3", "schematic")
```

## Target Directory Structure

```text
openpcbdb/
  __init__.py

  design/
    __init__.py
    database.py        # OpenPCBDB database handle
    properties.py      # design properties
    requirements.py    # requirements access
    context.py         # AI context APIs

  library/
    __init__.py
    lib.py             # Lib object
    tech.py            # Tech access
    index.py           # library.db operations

  cell/
    __init__.py
    cell.py            # Cell object
    properties.py      # cell.db properties
    hierarchy.py       # parent/child hierarchy helpers

  views/
    __init__.py
    base.py            # base View object
    symbol.py          # SymbolView / ports
    schematic.py       # SchematicView / insts / nets
    layout.py          # LayoutView / placement / routing / DRC
    netlist.py         # NetlistView
    bom.py             # BomView
    spice.py           # SpiceView
    verilog.py         # VerilogView
    manufacturing.py   # ManufacturingView

  objects/
    __init__.py
    inst.py            # CellInst / ComponentInst
    net.py             # Net / Connection
    port.py            # Port / Interface
    constraint.py      # View-local constraints
    toolView.py        # Tool-specific EDA view representation
    bomItem.py         # BOM item object

  oa/
    __init__.py
    dbObject.py        # common database object base
    dbRef.py           # lib/cell/view references
    dbPath.py          # path resolution
    dbIndex.py         # design.openPCBDB index

  io/
    __init__.py
    jsonDb.py          # read/write .db JSON files
    transactions.py    # save/rollback support

  check/
    __init__.py
    lcvCheck.py        # lib/cell/view hierarchy checks
    symbolCheck.py     # symbol contract checks
    schematicCheck.py  # schematic ERC checks
    layoutCheck.py     # layout/DRC checks
    techCheck.py       # technology/process checks

  translators/
    __init__.py
    kicad.py
    altium.py
    conceptHdl.py
    spice.py
    verilog.py

  cli.py
  errors.py
```

## Naming Rules

Use EDA-style names everywhere in the Python API.

```text
Classes:    PascalCase
Methods:    camelBack
Functions:  camelBack
Arguments:  camelBack
Constants:  UPPER_CASE
Modules:    EDA-oriented names
```

Examples:

```python
db.readLib(libName)
db.readCell(libName, cellName)
db.readView(libName, cellName, viewName)
cell.createView(viewName)
schematic.createCellInst(instName, libName, cellName)
net.connect(instName, portName)
```

## Core Object Model

```text
OpenPCBDB
  Lib
    Cell
      View
        ToolView
```

Supporting objects:

```text
Tech
Requirements
Port
Net
CellInst
ComponentInst
Constraint
ValidationReport
```

## Current Transitional State

The package currently still contains early prototype files:

```text
model.py
```

These should be split gradually.

The storage layer has already been separated into:

```text
openpcbdb/io/
  store.py
  jsonDb.py
```

Current storage is JSON, but the `DbStore` interface is intended to allow a future SQLite implementation without changing the EDA-level API.

Recommended migration order:

```text
1. design/database.py      extract OpenPCBDB database handle from model.py
2. library/lib.py          extract Lib
3. cell/cell.py            extract Cell
4. views/base.py           extract base View
5. views/schematic.py      add schematic-specific API
6. views/layout.py         add layout-specific API
7. views/netlist.py        add netlist-specific API
8. views/bom.py            add BOM-specific API
9. objects/*               extract Inst/Net/Port/Constraint/ToolView
10. io/jsonDb.py           keep JSON read/write behind DbStore
11. oa/*                   add common DB object/ref/path/index helpers
12. check/*                move validators
13. translators/*          add KiCad/Altium/ConceptHDL/SPICE/Verilog support
```

## Design Principle

`design.openPCBDB` is the design database index. It should contain the paths needed to access libraries, technologies, cells, and views.

The Python API should read the database through this index first. It should not depend on walking directories unless explicitly requested for repair or discovery.
