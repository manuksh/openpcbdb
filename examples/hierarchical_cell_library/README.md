# Hierarchical Cell Library Example

This example uses an EDA-style hierarchy:

```text
library / cell / view
```

A cell is the reusable design unit. A cell can be:

- `leaf`: implemented with real components in its own `schematic/view.db`.
- `composite`: implemented by instantiating other cells.

Each cell has a stable cell name, such as `amplifier`, `STM32_MCU_1123`, `usb_input`, or `buck_3v3`.

Directory structure:

```text
hierarchical_cell_library/
  design.openPCBDB
  requirements.db
  lib_1/
    library.db
    technology.db
    power_system/
      cell.db
      symbol/
        view.db
      schematic/
        view.db
      layout/
        view.db
    usb_input/
      cell.db
      symbol/
        view.db
      schematic/
        view.db
      layout/
        view.db
    buck_3v3/
      cell.db
      symbol/
        view.db
      schematic/
        view.db
      layout/
        view.db
  lib_2/
    library.db
    technology.db
    buck_3v3/
      cell.db
      symbol/
        view.db
      schematic/
        view.db
      layout/
        view.db
```

File roles:

```text
technology.db      fab/process specification for the library
cell.db            cell identity, version, library identity, view refs
symbol/view.db     public logical interface of the cell
schematic/view.db  implementation: components for leaf cells, cell instances for composite cells
layout/view.db     physical implementation or floorplan
```

Cell names are scoped by library. For example, `lib_1/buck_3v3` and `lib_2/buck_3v3` are different cells even though their cell names match.

Important hierarchy rule:

```text
Parent cells connect to child cells only through child symbol view ports.
```

Planning is top-down:

```text
requirements.db -> lib_1/power_system -> lib_1/usb_input + lib_1/buck_3v3
```

Validation is bottom-up:

```text
1. Validate leaf cells.
2. Validate each leaf schematic against its symbol.
3. Validate composite cell instances against referenced child symbols.
4. Validate composite schematic connections.
5. Validate requirements coverage.
6. Validate layout against schematic connectivity.
```
