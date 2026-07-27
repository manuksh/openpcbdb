# Skill: Edit Schematic View

Use this skill when editing logical connectivity, nets, component instances, or
cell instances.

## View ownership

Schematic data belongs in:

```text
libName/cellName/schematic/view.db
```

## Common API calls

```python
schematic = db.readSchematicView("lib_1", "power_system")

schematic.createNet("PWR_3V3")

schematic.createCellInst(
    instName="X_BUCK_3V3",
    libName="lib_1",
    cellName="buck_3v3",
    viewBinding={
        "symbol": "symbol",
        "schematic": "schematic",
        "layout": "layout",
    },
)

schematic.connect(
    netName="PWR_3V3",
    connection={
        "instance": "X_BUCK_3V3",
        "port": "VOUT",
    },
)
```

## Rules

- Create nets before connecting to them.
- Preserve instance names.
- Use `CellInstance` for subcells.
- Use `ComponentInstance` for physical/electrical parts.
- Keep schematic constraints in schematic view.
- Do not place routing or geometry here.

## Validation

After schematic edits:

```python
report = db.checkSchematic("lib_1", "power_system")
report.raiseIfBlocking()
```

