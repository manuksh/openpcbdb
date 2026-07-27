from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from openpcbdb import (
    OpenPCBDB,
    createAltiumToolView,
    createConceptHdlToolView,
    createKiCadToolView,
    createSpiceToolView,
    createVerilogToolView,
    exportKiCadSchematic,
)


class TranslatorApiTest(unittest.TestCase):
    def testCreateToolViewHelpers(self) -> None:
        with tempfile.TemporaryDirectory() as tempDir:
            db = OpenPCBDB.create(Path(tempDir), name="translator_test")
            db.createLibrary("lib_1")
            cell = db.createCell("lib_1", "logic_cell")
            schematic = cell.createView("schematic")

            createKiCadToolView(schematic, "toolViews/kicad/view.kicad_sch", "kicad_sch")
            createAltiumToolView(schematic, "toolViews/altium/view.SchDoc", "schdoc")
            createConceptHdlToolView(schematic, "toolViews/concept/view.cpm")
            createSpiceToolView(schematic, "toolViews/spice/view.sp")
            createVerilogToolView(schematic, "toolViews/verilog/view.v")

            toolNames = {toolView["tool"] for toolView in schematic.readToolViews()}

            self.assertIn("kicad", toolNames)
            self.assertIn("altium_designer", toolNames)
            self.assertIn("concept_hdl", toolNames)
            self.assertIn("spice", toolNames)
            self.assertIn("verilog", toolNames)

    def testTranslatorImportExportStubsAreExplicit(self) -> None:
        with self.assertRaises(NotImplementedError):
            exportKiCadSchematic(None, "lib_1", "cell_1", "out.kicad_sch")


if __name__ == "__main__":
    unittest.main()
