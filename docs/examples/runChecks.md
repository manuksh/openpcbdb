# Run checks

Checks validate the database structure and EDA contracts.

```python
from openpcbdb import OpenPCBDB

db = OpenPCBDB.open("examples/hierarchical_cell_library")

report = db.checkDesign()

print(report.summary())
report.raiseIfBlocking()
```

Run narrower checks:

```python
db.checkLcv()
db.checkTech("lib_1")
db.checkSymbol("lib_1", "buck_3v3")
db.checkSchematic("lib_1", "power_system")
db.checkLayout("lib_1", "power_system")
```

Typical check layers:

- `checkLcv`: library/cell/view path and hierarchy consistency.
- `checkTech`: technology database and process capability checks.
- `checkSymbol`: public port contract checks.
- `checkSchematic`: schematic ERC-style checks.
- `checkLayout`: layout/DRC-style checks.
