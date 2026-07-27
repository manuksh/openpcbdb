# OpenPCBDB AI Agent Pack

This directory contains project-local instructions for AI agents that work with
OpenPCBDB databases and the OpenPCBDB Python API.

It is intentionally separate from the Python package:

- `openpcbdb/` contains executable Python API code.
- `specification/` describes the database file format.
- `docs/` describes user-facing API documentation.
- `agents/` describes how AI agents should operate on OpenPCBDB designs.

## Directory structure

```text
agents/
  README.md
  skills/
    openpcbdb-eda-agent.md
    read-design-context.md
    create-cell-view.md
    edit-schematic-view.md
    edit-layout-view.md
    create-tool-view.md
    run-design-checks.md
  rules/
    naming-style.md
    database-integrity.md
    cell-view-paradigm.md
    ai-workflow.md
    validation.md
```

## How an AI agent should use this pack

Start with:

1. `skills/openpcbdb-eda-agent.md`
2. `rules/cell-view-paradigm.md`
3. `rules/database-integrity.md`
4. A task-specific skill from `skills/`

For any write operation, the agent must run the relevant checks from
`rules/validation.md`.

