from pathlib import Path
import unittest

from openpcbdb import Workspace


class WorkspaceTests(unittest.TestCase):
    def test_example_workspace_loads_and_validates(self) -> None:
        workspace = Workspace.open(
            Path("examples/hierarchical_cell_library/design.openPCBDB")
        )

        self.assertEqual(workspace.requirements()["type"], "Requirements")
        self.assertEqual(workspace.top_cell().name, "power_system")
        self.assertEqual(workspace.top_view().type, "Schematic")

        report = workspace.validate()

        self.assertEqual([], [result.message for result in report.errors])

    def test_can_navigate_library_cell_view(self) -> None:
        workspace = Workspace.open(
            Path("examples/hierarchical_cell_library/design.openPCBDB")
        )

        cell = workspace.library("lib_2").cell("buck_3v3")
        view = cell.view("layout")

        self.assertEqual("lib_2", cell.library.name)
        self.assertEqual("PCBLayout", view.type)
        self.assertEqual("buck_3v3", view.data["cell"])

    def test_can_open_workspace_directory_and_read_design_index(self) -> None:
        workspace = Workspace.open(Path("examples/hierarchical_cell_library"))

        index = workspace.read_design_index()
        view_index = workspace.view_index("lib_1", "power_system", "schematic")

        self.assertEqual("Project", index["type"])
        self.assertEqual("lib_1/power_system/schematic/view.db", view_index["path"])

    def test_read_cell_properties_uses_design_database(self) -> None:
        workspace = Workspace.open(Path("examples/hierarchical_cell_library"))

        properties = workspace.read_cell_properties("lib_1", "buck_3v3")

        self.assertEqual("Cell", properties["type"])
        self.assertEqual("buck_3v3", properties["cell"])


if __name__ == "__main__":
    unittest.main()
