# Skill: Read Design Context

Use this skill before planning or changing an OpenPCBDB design.

## Goal

Give the AI agent enough semantic design context without forcing it to open
every database file manually.

## Workflow

```python
from openpcbdb import OpenPCBDB

db = OpenPCBDB.open("path/to/design")
designContext = db.readDesignContext(depth=1)
```

For a focused task:

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
```

## Agent behavior

- Read context first.
- Identify top cell, libraries, child cells, and relevant views.
- Prefer `readCellContext` over many small reads when reasoning semantically.
- Use deeper context only when the hierarchy decision requires it.
- After reading context, state the intended edit target before writing.

