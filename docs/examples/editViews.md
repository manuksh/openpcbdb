# Edit views

Each view owns the data that belongs to that view. Symbol ports belong to
`symbol/view.db`, electrical nets belong to `schematic/view.db`, and physical
constraints belong to `layout/view.db`.

## Symbol ports

```python
from openpcbdb import OpenPCBDB

db = OpenPCBDB.open("examples/hierarchical_cell_library")
symbol = db.readSymbolView("lib_1", "buck_3v3")

symbol.createPort(
    portName="VIN",
    direction="input",
    electricalType="power",
    properties={
        "description": "Input supply voltage",
    },
)

print(symbol.readPorts())
```

## Schematic nets and instances

```python
schematic = db.readSchematicView("lib_1", "power_system")

schematic.createNet(
    netName="PWR_3V3",
    properties={
        "semantic": {
            "purpose": "Main 3.3 V system rail",
        },
    },
)

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

## Layout placement and constraints

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
    constraintName="minBuckKeepout",
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
