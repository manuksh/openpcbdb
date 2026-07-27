# AI Agent Pack

OpenPCBDB includes project-local AI agent instructions in:

```text
agents/
  skills/
  rules/
```

These files are not runtime Python API code. They are operating instructions
for AI agents that modify OpenPCBDB designs.

## Main entry point

Start with:

```text
agents/skills/openpcbdb-eda-agent.md
```

Then load the rule files required for the task:

```text
agents/rules/cell-view-paradigm.md
agents/rules/database-integrity.md
agents/rules/naming-style.md
agents/rules/ai-workflow.md
agents/rules/validation.md
```

## Task-specific skills

```text
agents/skills/read-design-context.md
agents/skills/create-cell-view.md
agents/skills/edit-schematic-view.md
agents/skills/edit-layout-view.md
agents/skills/create-tool-view.md
agents/skills/run-design-checks.md
```

## Design intent

The agent pack teaches an AI agent to work like an EDA database engineer:

- open `design.openPCBDB` through the Python API
- preserve library/cell/view hierarchy
- keep constraints in the correct view
- use `toolView` for EDA-specific representations
- run checks after writes
- report changed files and validation results

