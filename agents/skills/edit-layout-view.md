# Skill: Edit Layout View

Use this skill when editing placement, routing, physical constraints, DRC data,
or manufacturing-facing physical implementation.

## View ownership

Layout data belongs in:

```text
libName/cellName/layout/view.db
```

Technology/process limits belong in:

```text
libName/technology.db
```

## Common API calls

```python
layout = db.readLayoutView("lib_1", "power_system")

layout.createPlacement(
    targetName="X_BUCK_3V3",
    x=20.0,
    y=15.0,
    unit="mm",
    properties={
        "rotation": 0,
        "side": "top",
    },
)

layout.createConstraint(
    constraintName="buckKeepout",
    constraintType="placementKeepout",
    properties={
        "target": "X_BUCK_3V3",
        "clearance": {
            "value": 2.0,
            "unit": "mm",
        },
    },
)
```

## Rules

- Keep physical constraints in layout view.
- Check the library technology before changing layer, via, clearance, or stackup assumptions.
- Do not encode schematic connectivity only in layout.
- Keep routing associated with schematic net names.
- Do not invent fab limits; read `technology.db`.

## Validation

After layout edits:

```python
db.checkTech("lib_1").raiseIfBlocking()
db.checkLayout("lib_1", "power_system").raiseIfBlocking()
```

