# Skill: OpenPCBDB EDA Agent

Use this skill when acting as an AI design agent for an OpenPCBDB project.

The agent must behave like an EDA database engineer, not like a generic JSON
editor.

## Core model

OpenPCBDB follows the library/cell/view paradigm:

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

The main Python API entry point is:

```python
from openpcbdb import OpenPCBDB

db = OpenPCBDB.open("path/to/design")
```

## Operating rules

Always follow:

- `../rules/cell-view-paradigm.md`
- `../rules/database-integrity.md`
- `../rules/naming-style.md`
- `../rules/ai-workflow.md`
- `../rules/validation.md`

## Default workflow

1. Open the design database with `OpenPCBDB.open`.
2. Read `design.openPCBDB` through API calls, not manual JSON parsing.
3. Read AI context before modifying design intent.
4. Modify the smallest correct database object.
5. Preserve library/cell/view identity.
6. Run checks.
7. Report exactly what changed.

## Preferred API pattern

Use `read*` for database reads:

```python
db.readLib("lib_1")
db.readCell("lib_1", "buck_3v3")
db.readSchematicView("lib_1", "power_system")
```

Use `create*` for database writes:

```python
cell.createView("schematic")
schematic.createNet("PWR_3V3")
layout.createPlacement("X_BUCK_3V3", 20.0, 15.0)
```

## Do not

- Do not invent a second hierarchy model.
- Do not call tool-specific representations `backend`.
- Do not bypass `design.openPCBDB` indexes unless repairing a broken database.
- Do not put layout constraints in schematic views.
- Do not put schematic constraints in layout views.
- Do not edit generated tool files when the semantic OpenPCBDB view is the source of truth.

