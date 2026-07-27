# Create a cell and views

Create cells through the design database or through a library handle.

```python
from openpcbdb import OpenPCBDB

db = OpenPCBDB.open("examples/hierarchical_cell_library")

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

The resulting database follows the cell/view structure:

```text
lib_1/
  analog_amplifier/
    cell.db
    symbol/view.db
    schematic/view.db
    layout/view.db
```

You can also access the same objects through `read*` calls:

```python
sameCell = db.readCell("lib_1", "analog_amplifier")
sameSymbol = db.readSymbolView("lib_1", "analog_amplifier")
```
