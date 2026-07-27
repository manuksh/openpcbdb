# API usage

The Python API is the programmable EDA interface to `design.openPCBDB`.

It should let an AI agent or script open a design database once, then access
libraries, cells, views, technology, requirements, and checks through stable
objects instead of manually parsing many JSON files.

## Main object flow

```text
OpenPCBDB
  readLib("lib_1") -> Lib
    readCell("buck_3v3") -> Cell
      readView("schematic") -> SchematicView
      readView("layout")    -> LayoutView
```

## Design rule for API authors

Keep file format and storage behind the IO layer. Today the storage is JSON
because AI agents can read it directly. Later the same API can read SQLite or
binary databases without changing user scripts.
