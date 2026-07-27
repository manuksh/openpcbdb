# Skill: Create Cell and Views

Use this skill when creating a new OpenPCBDB cell or adding views to an
existing cell.

## Workflow

```python
from openpcbdb import OpenPCBDB

db = OpenPCBDB.open("path/to/design")

cell = db.createCell(
    libName="lib_1",
    cellName="analog_amplifier",
    cellType="leaf",
    name="Analog Amplifier",
)

symbol = cell.createView("symbol")
schematic = cell.createView("schematic")
layout = cell.createView("layout")
```

## Required decisions

Before creating a cell, determine:

- target library
- cell name
- whether the cell is `leaf` or `hierarchical`
- required views
- technology compatibility

## Rules

- A cell must live inside exactly one library.
- A cell must have `cell.db`.
- Each view must live in its own directory as `view.db`.
- A hierarchical cell may instantiate child cells in schematic view.
- A leaf cell may have direct component instances, layout, and manufacturing data.

## Validation

After creating cells/views:

```python
report = db.checkLcv()
report.raiseIfBlocking()
```

