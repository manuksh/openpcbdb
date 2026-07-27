import unittest

from openpcbdb import OpenPCBDB


class DesignContextTests(unittest.TestCase):
    def test_read_design_context_default(self) -> None:
        db = OpenPCBDB.open("examples/hierarchical_cell_library")

        context = db.readDesignContext()

        self.assertIn("properties", context)
        self.assertIn("requirementsRef", context)
        self.assertIn("libraries", context)
        self.assertIn("top", context)

    def test_read_design_context_with_depth(self) -> None:
        db = OpenPCBDB.open("examples/hierarchical_cell_library")

        context = db.readDesignContext(depth=1)

        self.assertIn("topCellContext", context)
        self.assertEqual("power_system", context["topCellContext"]["cell"])

    def test_read_cell_context_sections(self) -> None:
        db = OpenPCBDB.open("examples/hierarchical_cell_library")

        context = db.readCellContext(
            libName="lib_1",
            cellName="power_system",
            depth=1,
            include=["cell", "views", "symbol", "schematic", "constraints"],
        )

        self.assertEqual("lib_1", context["library"])
        self.assertEqual("power_system", context["cell"])
        self.assertIn("cellProperties", context)
        self.assertIn("symbol", context)
        self.assertIn("schematic", context)
        self.assertIn("children", context)

    def test_read_view_context_and_hierarchy_context(self) -> None:
        db = OpenPCBDB.open("examples/hierarchical_cell_library")

        viewContext = db.readViewContext("lib_1", "buck_3v3", "layout")
        hierarchyContext = db.readHierarchyContext("lib_1", "power_system", depth=1)

        self.assertEqual("layout", viewContext["view"])
        self.assertIn("toolViews", viewContext)
        self.assertIn("children", hierarchyContext)


if __name__ == "__main__":
    unittest.main()
