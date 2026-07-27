# Documentation style

OpenPCBDB documentation should be generated from real Python code wherever
possible.

## Source of truth

- `specification/specification.md` describes the database file format.
- `docs/` describes how to use the Python API.
- Python docstrings describe classes, methods, arguments, return values, and
  EDA behavior.

## Naming style

Use EDA-style `camelBack` for public APIs:

```python
db.readCell("lib_1", "buck_3v3")
db.readSchematicView("lib_1", "power_system")
cell.createView("layout")
```

Do not introduce generic software terms when an EDA term exists. Prefer:

- `toolView`, not backend
- `Lib`, `Cell`, `View`, `Tech`
- `read*` for database reads
- `check*` for database validation

## Docstring format

Use Google-style docstrings:

```python
def readCell(self, libName: str, cellName: str) -> Cell:
    """Read a cell handle.

    Args:
        libName: Library name from `design.openPCBDB`.
        cellName: Cell name inside `library.db`.

    Returns:
        Typed `Cell` object.
    """
```

This lets `mkdocstrings` generate API reference pages automatically.
