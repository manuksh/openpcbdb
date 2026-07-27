from pathlib import Path
import shutil
import tempfile
import unittest

from openpcbdb import OpenPCBDB
from openpcbdb.check import (
    checkDesign,
    checkLayout,
    checkLcv,
    checkSchematic,
    checkSymbol,
    checkTech,
)
from openpcbdb.io import loadJsonFile, saveJsonFile


class CheckModulesTests(unittest.TestCase):
    def test_clean_example_passes_all_check_modules(self) -> None:
        db = OpenPCBDB.open("examples/hierarchical_cell_library")

        reports = [
            checkLcv(db),
            checkTech(db, "lib_1"),
            checkSymbol(db, "lib_1", "buck_3v3"),
            checkSchematic(db, "lib_1", "power_system"),
            checkLayout(db, "lib_1", "buck_3v3"),
            checkDesign(db),
            db.checkDesign(),
            db.checkTech("lib_1"),
            db.checkSymbol("lib_1", "buck_3v3"),
            db.checkSchematic("lib_1", "power_system"),
            db.checkLayout("lib_1", "buck_3v3"),
        ]

        for report in reports:
            self.assertEqual([], [result.message for result in report.errors])

    def test_symbol_check_finds_duplicate_ports(self) -> None:
        with tempfile.TemporaryDirectory() as tmpDir:
            dst = _copyExample(tmpDir)
            symbolPath = dst / "lib_1" / "buck_3v3" / "symbol" / "view.db"
            data = loadJsonFile(symbolPath)
            data["ports"].append(dict(data["ports"][0]))
            saveJsonFile(symbolPath, data)

            report = checkSymbol(OpenPCBDB.open(dst), "lib_1", "buck_3v3")

            self.assertTrue(any("Duplicate symbol port" in item.message for item in report.errors))

    def test_schematic_check_finds_missing_child_port(self) -> None:
        with tempfile.TemporaryDirectory() as tmpDir:
            dst = _copyExample(tmpDir)
            schematicPath = dst / "lib_1" / "power_system" / "schematic" / "view.db"
            data = loadJsonFile(schematicPath)
            data["nets"][0]["connections"][1]["port"] = "missing_port"
            saveJsonFile(schematicPath, data)

            report = checkSchematic(OpenPCBDB.open(dst), "lib_1", "power_system")

            self.assertTrue(any("missing port" in item.message for item in report.errors))

    def test_tech_check_finds_invalid_via_layer(self) -> None:
        with tempfile.TemporaryDirectory() as tmpDir:
            dst = _copyExample(tmpDir)
            techPath = dst / "lib_1" / "technology.db"
            data = loadJsonFile(techPath)
            data["vias"][0]["allowedLayers"].append("BAD_LAYER")
            saveJsonFile(techPath, data)

            report = checkTech(OpenPCBDB.open(dst), "lib_1")

            self.assertTrue(any("unknown layer BAD_LAYER" in item.message for item in report.errors))


def _copyExample(tmpDir: str) -> Path:
    src = Path("examples/hierarchical_cell_library")
    dst = Path(tmpDir) / "designCopy"
    shutil.copytree(src, dst)
    return dst


if __name__ == "__main__":
    unittest.main()
