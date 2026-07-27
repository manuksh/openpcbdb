# Add toolViews

`toolView` entries attach EDA tool-specific representations to a logical
OpenPCBDB view.

This lets one cell view have physical realizations in different EDA tools
without changing the semantic OpenPCBDB database.

```python
from openpcbdb import OpenPCBDB

db = OpenPCBDB.open("examples/hierarchical_cell_library")

schematic = db.readSchematicView("lib_1", "buck_3v3")
layout = db.readLayoutView("lib_1", "buck_3v3")

schematic.createToolView(
    tool="kicad",
    format="kicad_sch",
    path="toolViews/kicad/view.kicad_sch",
    role="derived",
)

layout.createToolView(
    tool="altium_designer",
    format="pcbdoc",
    path="toolViews/altium/view.PcbDoc",
    role="snapshot",
)

print(schematic.readToolViews())
print(layout.readToolViews())
```

Recommended roles:

- `native`: primary editable representation for that tool.
- `derived`: generated from OpenPCBDB semantic data.
- `snapshot`: imported or frozen tool state.

Use `toolView`, not backend. In EDA terms, this is a tool-specific view of the
same cell/view database object.
