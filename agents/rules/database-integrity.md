# Rule: Database Integrity

Do not treat OpenPCBDB as unrelated JSON files. Treat it as an indexed EDA
database.

## Required invariants

- `design.openPCBDB` is the design index.
- `design.openPCBDB` must contain library/cell/view references needed to open the hierarchy.
- `library.db` indexes cells in a library.
- `cell.db` indexes views in a cell.
- `view.db` stores the data for exactly one cell view.
- Relative paths must remain valid from the file that owns the reference.

## Write discipline

Before writing:

1. Open the design through `OpenPCBDB.open`.
2. Locate the owner object.
3. Use API methods when available.
4. Write only the smallest correct object.
5. Run relevant checks.

## Do not

- Do not hand-edit multiple indexes unless the API cannot express the change.
- Do not create orphan views not referenced by `cell.db`.
- Do not create orphan cells not referenced by `library.db` and `design.openPCBDB`.
- Do not move files without updating references.
- Do not change identity fields casually.

