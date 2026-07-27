from __future__ import annotations

from typing import Any

from openpcbdb.model import ValidationReport


def checkTech(db: Any, libName: str) -> ValidationReport:
    """Check a library technology database."""
    report = ValidationReport()
    try:
        tech = db.readLib(libName).readTech()
    except Exception as exc:
        report.add("error", f"Cannot read technology for {libName}: {exc}", db.path)
        return report

    data = tech.readProperties()
    if data.get("type") != "Technology":
        report.add("error", f"Technology type must be Technology for {libName}", tech.path)
    if data.get("library") != libName:
        report.add("error", f"Technology library mismatch for {libName}", tech.path)

    stackup = tech.readStackup()
    layers = stackup.get("layers", [])
    if not isinstance(layers, list) or not layers:
        report.add("error", f"Technology {libName} has no stackup layers", tech.path)
        return report

    layerIds: list[str] = []
    for layer in layers:
        if not isinstance(layer, dict):
            report.add("error", f"Technology {libName} has invalid layer entry", tech.path)
            continue
        layerId = layer.get("id")
        if not isinstance(layerId, str) or not layerId:
            report.add("error", f"Technology {libName} has layer without id", tech.path)
            continue
        if layerId in layerIds:
            report.add("error", f"Duplicate technology layer id {layerId}", tech.path)
        layerIds.append(layerId)

    layerSet = set(layerIds)
    vias = data.get("vias", [])
    if isinstance(vias, list):
        for via in vias:
            if not isinstance(via, dict):
                continue
            for layerId in via.get("allowedLayers", []):
                if layerId not in layerSet:
                    report.add("error", f"Via {via.get('id')} references unknown layer {layerId}", tech.path)

    _checkRulePair(data, "traceWidth", report, tech.path)
    _checkRulePair(data, "traceSpacing", report, tech.path)
    return report


def _checkRulePair(data: dict[str, Any], ruleName: str, report: ValidationReport, path: Any) -> None:
    rules = data.get("designRules", {})
    if not isinstance(rules, dict):
        report.add("error", "Technology designRules must be an object", path)
        return
    rule = rules.get(ruleName)
    if not isinstance(rule, dict):
        report.add("warning", f"Technology has no {ruleName} rule", path)
        return
    absolute = _readValue(rule.get("absoluteMinimum"))
    preferred = _readValue(rule.get("preferredDefault"))
    if absolute is not None and preferred is not None and preferred < absolute:
        report.add("error", f"{ruleName}.preferredDefault is below absoluteMinimum", path)


def _readValue(value: Any) -> float | None:
    if isinstance(value, dict) and isinstance(value.get("value"), (int, float)):
        return float(value["value"])
    return None
