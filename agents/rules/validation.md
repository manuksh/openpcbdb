# Rule: Validation

Every AI agent write operation should end with checks proportional to the
change.

## Check mapping

| Change | Required check |
| --- | --- |
| create library/cell/view | `checkLcv` |
| edit symbol ports | `checkSymbol` |
| edit schematic nets/instances | `checkSchematic` |
| edit layout placement/routing/constraints | `checkLayout` |
| edit technology/process data | `checkTech` |
| broad design change | `checkDesign` |

## Python pattern

```python
report = db.checkDesign()
print(report.summary())
report.raiseIfBlocking()
```

## Handoff

Final response after edits must include:

- what changed
- which files changed
- which checks were run
- remaining risks or assumptions

