from pathlib import Path
import shutil
import tempfile
import unittest

from openpcbdb import (
    BomView,
    LayoutView,
    Lib,
    OpenPCBDB,
    SchematicView,
    SymbolView,
    Tech,
)


class LibraryCellViewsTests(unittest.TestCase):
    def test_read_typed_library_cell_and_views(self) -> None:
        db = OpenPCBDB.open("examples/hierarchical_cell_library")

        lib = db.readLib("lib_1")
        cell = db.readCell("lib_1", "buck_3v3")
        symbol = db.readSymbolView("lib_1", "buck_3v3")
        schematic = db.readSchematicView("lib_1", "buck_3v3")
        layout = db.readLayoutView("lib_1", "buck_3v3")

        self.assertIsInstance(lib, Lib)
        self.assertIsInstance(lib.readTech(), Tech)
        self.assertEqual("TECH_JLCPCB_6L_STD_1OZ", lib.readTech().readProperties()["id"])
        self.assertEqual("buck_3v3", cell.readCellName())
        self.assertIsInstance(symbol, SymbolView)
        self.assertIsInstance(schematic, SchematicView)
        self.assertIsInstance(layout, LayoutView)

    def test_symbol_schematic_and_layout_operations(self) -> None:
        with tempfile.TemporaryDirectory() as tmpDir:
            src = Path("examples/hierarchical_cell_library")
            dst = Path(tmpDir) / "designCopy"
            shutil.copytree(src, dst)
            db = OpenPCBDB.open(dst)

            symbol = db.readSymbolView("lib_1", "buck_3v3")
            schematic = db.readSchematicView("lib_1", "buck_3v3")
            layout = db.readLayoutView("lib_1", "buck_3v3")

            symbol.createPort("pgood", "output", "digital")
            schematic.createNet("NET_TEST", name="TEST")
            schematic.connect("NET_TEST", {"externalPort": "pgood"})
            layout.createPlacement("TP1", x=1.0, y=2.0)
            layout.createToolView(
                tool="kicad",
                format="kicad_pcb",
                path="toolViews/kicad/view.kicad_pcb",
            )

            self.assertEqual("pgood", symbol.readPort("pgood")["id"])
            self.assertEqual("TEST", schematic.readNet("NET_TEST")["name"])
            self.assertEqual(1, len(layout.readToolViews()))
            self.assertTrue(any(item.get("refDesignator") == "TP1" for item in layout.readPlacements()))

    def test_create_cell_and_bom_view(self) -> None:
        with tempfile.TemporaryDirectory() as tmpDir:
            db = OpenPCBDB.create(Path(tmpDir), name="Scratch")
            db.createLibrary("worklib")
            cell = db.createCell("worklib", "bom_test")
            bom = db.createView("worklib", "bom_test", "bom")

            self.assertIsInstance(bom, BomView)
            bom.addItem({"mpn": "TEST", "quantity": 1})

            reloadedBom = db.readView("worklib", "bom_test", "bom")
            self.assertIsInstance(reloadedBom, BomView)
            self.assertEqual("TEST", reloadedBom.readItems()[0]["mpn"])
            self.assertIn("bom", db.readCell("worklib", "bom_test").readViews())


if __name__ == "__main__":
    unittest.main()
