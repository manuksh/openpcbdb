from pathlib import Path
import shutil
import tempfile
import unittest

from openpcbdb import OpenPCBDB


class DesignRequirementsTests(unittest.TestCase):
    def test_read_requirements_and_ref(self) -> None:
        db = OpenPCBDB.open("examples/hierarchical_cell_library")

        self.assertEqual("REQ_POWER_SYSTEM_0001", db.readRequirements()["id"])
        self.assertEqual("requirements.db", db.readRequirementsRef()["file"])

    def test_set_requirements_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmpDir:
            src = Path("examples/hierarchical_cell_library")
            dst = Path(tmpDir) / "designCopy"
            shutil.copytree(src, dst)

            db = OpenPCBDB.open(dst)
            db.setRequirementsRef(
                file="requirements.db",
                id="REQ_POWER_SYSTEM_0001",
                version="0.2.0",
                hash="sha256:test",
            )
            ref = OpenPCBDB.open(dst).readRequirementsRef()

            self.assertEqual("0.2.0", ref["version"])
            self.assertEqual("sha256:test", ref["hash"])


if __name__ == "__main__":
    unittest.main()
