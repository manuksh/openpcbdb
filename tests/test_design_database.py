from pathlib import Path
import tempfile
import unittest

from openpcbdb import OpenPCBDB


class DesignDatabaseTests(unittest.TestCase):
    def test_open_accepts_design_file_or_directory(self) -> None:
        designPath = Path("examples/hierarchical_cell_library/design.openPCBDB")

        fromFile = OpenPCBDB.open(designPath)
        fromDirectory = OpenPCBDB.open(designPath.parent)

        self.assertEqual(designPath.resolve(), fromFile.path)
        self.assertEqual(designPath.resolve(), fromDirectory.path)

    def test_create_writes_design_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpDir:
            db = OpenPCBDB.create(Path(tmpDir), name="Scratch Design")

            self.assertEqual("Scratch Design", db.readDesignName())
            self.assertTrue((Path(tmpDir) / "design.openPCBDB").exists())
            self.assertEqual("worklib", db.readTop()["library"])
            self.assertEqual("top", db.readTop()["cell"])

    def test_read_design_database_objects(self) -> None:
        db = OpenPCBDB.open("examples/hierarchical_cell_library")

        self.assertEqual(2, len(db.readLibraries()))
        self.assertEqual("Library", db.readLibraryProperties("lib_1")["type"])
        self.assertEqual("Cell", db.readCellProperties("lib_1", "buck_3v3")["type"])
        self.assertEqual("Schematic", db.readViewProperties("lib_1", "buck_3v3", "schematic")["type"])

    def test_read_specific_view_types(self) -> None:
        db = OpenPCBDB.open("examples/hierarchical_cell_library")

        self.assertEqual("CellSymbol", db.readSymbolView("lib_1", "buck_3v3").type)
        self.assertEqual("Schematic", db.readSchematicView("lib_1", "buck_3v3").type)
        self.assertEqual("PCBLayout", db.readLayoutView("lib_1", "buck_3v3").type)


if __name__ == "__main__":
    unittest.main()
