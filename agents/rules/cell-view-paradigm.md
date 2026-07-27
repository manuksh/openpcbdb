# Rule: Cell/View Paradigm

OpenPCBDB follows the EDA library/cell/view paradigm.

## Hierarchy

```text
Library
  Cell
    View
```

A cell is the reusable EDA design unit. A view is one representation of that
cell.

## Common views

- `symbol`: public interface/ports.
- `schematic`: logical connectivity and instances.
- `layout`: physical placement/routing/constraints.
- `netlist`: extracted or generated connectivity.
- `bom`: procurement/material view.
- `spice`: analog simulation view.
- `verilog`: digital logic view.
- `manufacturing`: fabrication/assembly outputs.

## Cell type

- `leaf`: direct component-level implementation.
- `hierarchical`: contains child `CellInstance` objects.

## Rule of ownership

- Ports belong to `symbol`.
- Nets and instances belong to `schematic`.
- Placement/routing/DRC belong to `layout`.
- Fab capabilities belong to `technology.db`.
- Product goals belong to `requirements.db`.

