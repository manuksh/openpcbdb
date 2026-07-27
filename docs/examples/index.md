# Examples

These examples show the intended EDA workflow for the Python API.

OpenPCBDB scripts should feel close to Virtuoso/OpenAccess-style database
scripting:

```text
db = OpenPCBDB.open(...)
lib = db.readLib(...)
cell = lib.readCell(...)
schematic = cell.readView("schematic")
```

The examples use the sample database in:

```text
examples/hierarchical_cell_library
```

## Example flow

1. Open `design.openPCBDB`.
2. Read libraries, cells, views, and AI context.
3. Create a new cell.
4. Create symbol/schematic/layout views.
5. Add ports, nets, instances, constraints, and toolViews.
6. Run EDA checks.

## Important convention

Use `read*` for database reads:

```python
db.readCell("lib_1", "buck_3v3")
db.readSchematicView("lib_1", "power_system")
```

Use `create*` for database writes:

```python
cell.createView("schematic")
schematic.createNet("VIN")
```
