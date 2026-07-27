# Rule: AI Workflow

AI agents should optimize for safe, explainable EDA database edits.

## Before editing

1. Read design context.
2. Identify target library/cell/view.
3. Identify whether the requested change is semantic, schematic, layout, toolView, or technology.
4. State the planned owner object.

## During editing

- Use Python API first.
- Keep modifications local to the responsible view.
- Preserve semantic reasoning fields when present.
- Add semantic fields when creating new design objects.
- Prefer stable IDs over display names.

## After editing

1. Run targeted checks.
2. Run full `checkDesign` for larger changes.
3. Report changed files and check results.

## When uncertain

Ask before changing:

- technology assumptions
- fab/process limits
- hierarchy boundaries
- identity/version fields
- source-of-truth ownership between OpenPCBDB and a toolView

