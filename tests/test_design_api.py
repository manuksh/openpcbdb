from pathlib import Path
import tempfile
import unittest

from openpcbdb import OpenPCBDB


class DesignApiTests(unittest.TestCase):
    def test_open_design_database_and_read_properties(self) -> None:
        db = OpenPCBDB.open(Path("examples/hierarchical_cell_library"))

        self.assertEqual("hierarchical_cell_library_example", db.readDesignId())
        self.assertEqual("Hierarchical Cell Library Example", db.readDesignName())
        self.assertEqual("0.1.0", db.readDesignVersion())
        self.assertEqual("Project", db.readDesignProperties()["type"])

    def test_read_libraries_cells_and_views(self) -> None:
        db = OpenPCBDB.open(Path("examples/hierarchical_cell_library"))

        self.assertEqual(2, len(db.readLibraries()))
        self.assertEqual("Library", db.readLibraryProperties("lib_1")["type"])
        self.assertEqual("buck_3v3", db.readCellProperties("lib_1", "buck_3v3")["cell"])
        self.assertEqual("Schematic", db.readSchematicView("lib_1", "buck_3v3").type)
        self.assertEqual("PCBLayout", db.readLayoutView("lib_1", "buck_3v3").type)
        self.assertEqual("CellSymbol", db.readSymbolView("lib_1", "buck_3v3").type)

    def test_read_requirements_and_context(self) -> None:
        db = OpenPCBDB.open(Path("examples/hierarchical_cell_library"))

        designContext = db.readDesignContext(depth=1)
        cellContext = db.readCellContext(
            libName="lib_1",
            cellName="power_system",
            depth=1,
            include=["cell", "views", "symbol", "schematic", "constraints"],
        )

        self.assertEqual("REQ_POWER_SYSTEM_0001", db.readRequirements()["id"])
        self.assertIn("topCellContext", designContext)
        self.assertEqual("power_system", cellContext["cell"])
        self.assertIn("symbol", cellContext)
        self.assertIn("schematic", cellContext)

    def test_create_design_database(self) -> None:
        with tempfile.TemporaryDirectory() as tmpDir:
            db = OpenPCBDB.create(Path(tmpDir), name="Scratch Design")

            self.assertEqual("Scratch Design", db.readDesignName())
            self.assertEqual((Path(tmpDir) / "design.openPCBDB").resolve(), db.path)


if __name__ == "__main__":
    unittest.main()
