# Skill: Create Tool View

Use this skill when attaching KiCad, Altium Designer, ConceptHDL, Virtuoso-like,
SPICE, Verilog, or other tool-specific representations to an OpenPCBDB view.

## Concept

`toolView` is a tool-specific representation of a semantic OpenPCBDB view.

Use `toolView`, not `backend`.

## Example

```python
schematic = db.readSchematicView("lib_1", "buck_3v3")

schematic.createToolView(
    tool="kicad",
    format="kicad_sch",
    path="toolViews/kicad/view.kicad_sch",
    role="derived",
)
```

Layout example:

```python
layout = db.readLayoutView("lib_1", "buck_3v3")

layout.createToolView(
    tool="altium_designer",
    format="pcbdoc",
    path="toolViews/altium/view.PcbDoc",
    role="snapshot",
)
```

## Roles

- `native`: primary editable representation for that tool.
- `derived`: generated from OpenPCBDB semantic data.
- `snapshot`: imported or frozen tool state.

## Rules

- Store tool-specific paths under the owning view.
- Do not make tool files the only source of semantic truth.
- Do not mix toolViews between cells or views.
- Preserve relative paths where possible.

