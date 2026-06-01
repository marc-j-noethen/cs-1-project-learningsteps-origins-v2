import importlib
import os
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "api"))


class AppImportTests(unittest.TestCase):
    def test_main_module_builds_fastapi_app(self):
        os.environ["DATABASE_URL"] = "postgresql://postgres:test-password@localhost:5432/testdb"
        os.environ["SESSION_SECRET"] = "0123456789abcdef0123456789abcdef"
        os.environ["SWB_ADMIN_PASSWORD"] = "test-password"
        os.environ["SWB_ALLOWED_HOSTS"] = "localhost,127.0.0.1,testserver"

        sys.modules.pop("main", None)
        main = importlib.import_module("main")

        self.assertEqual(main.app.title, "SWB | Second-Workshop-Brain")


if __name__ == "__main__":
    unittest.main()
