# Skill: Run Design Checks

Use this skill after reading, creating, or editing OpenPCBDB database objects.

## Full design check

```python
from openpcbdb import OpenPCBDB

db = OpenPCBDB.open("path/to/design")

report = db.checkDesign()
print(report.summary())
report.raiseIfBlocking()
```

## Targeted checks

```python
db.checkLcv()
db.checkTech("lib_1")
db.checkSymbol("lib_1", "buck_3v3")
db.checkSchematic("lib_1", "power_system")
db.checkLayout("lib_1", "power_system")
```

## Check selection

- Use `checkLcv` after creating libraries, cells, or views.
- Use `checkSymbol` after editing ports.
- Use `checkSchematic` after editing nets or instances.
- Use `checkLayout` after editing placement, routing, zones, or physical constraints.
- Use `checkTech` after changing technology/process assumptions.
- Use `checkDesign` before final handoff.

## Reporting

When reporting to a user, include:

- checks executed
- number of errors/warnings
- blocking failures, if any
- files changed

