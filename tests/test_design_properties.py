from pathlib import Path
import shutil
import tempfile
import unittest

from openpcbdb import OpenPCBDB


class DesignPropertiesTests(unittest.TestCase):
    def test_read_design_properties(self) -> None:
        db = OpenPCBDB.open("examples/hierarchical_cell_library")

        self.assertEqual("hierarchical_cell_library_example", db.readDesignId())
        self.assertEqual("Hierarchical Cell Library Example", db.readDesignName())
        self.assertEqual("0.1.0", db.readDesignVersion())
        self.assertEqual("Project", db.readDesignProperties()["type"])
        self.assertEqual(db.readDesignProperties(), db.readDesignIndex())

    def test_update_design_properties_and_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmpDir:
            src = Path("examples/hierarchical_cell_library")
            dst = Path(tmpDir) / "designCopy"
            shutil.copytree(src, dst)

            db = OpenPCBDB.open(dst)
            db.updateDesignProperties({"name": "Copied Design"})
            db.setDesignVersion("0.2.0")
            reloaded = OpenPCBDB.open(dst)

            self.assertEqual("Copied Design", reloaded.readDesignName())
            self.assertEqual("0.2.0", reloaded.readDesignVersion())


if __name__ == "__main__":
    unittest.main()
