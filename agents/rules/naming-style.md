# Rule: Naming Style

OpenPCBDB Python API uses EDA-style names.

## Public Python API

Use `camelBack` for public methods and arguments:

```python
readCell
readSchematicView
createToolView
libName
cellName
viewName
```

Use `PascalCase` for classes:

```python
OpenPCBDB
Lib
Cell
View
SchematicView
LayoutView
```

Use `UPPER_CASE` for constants.

## Terminology

Prefer EDA words:

- `Lib`, not package
- `Cell`, not module
- `View`, not file type
- `Tech`, not process config
- `toolView`, not backend
- `read*`, not `get*`
- `check*`, not validate-only generic names

## Database filenames

Use canonical filenames:

```text
design.openPCBDB
library.db
technology.db
cell.db
view.db
requirements.db
```

