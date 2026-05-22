import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "api"))

from security import generate_password_hash, slugify_title, verify_password


class SecurityTests(unittest.TestCase):
    def test_password_hash_roundtrip(self):
        password_hash = generate_password_hash("correct horse battery staple")
        self.assertTrue(
            verify_password(
                "correct horse battery staple",
                password_hash=password_hash,
            )
        )
        self.assertFalse(verify_password("wrong password", password_hash=password_hash))

    def test_slugify_title(self):
        self.assertEqual(slugify_title("Docker Compose verwenden"), "docker-compose-verwenden")
        self.assertEqual(slugify_title("SWB ###"), "swb")


if __name__ == "__main__":
    unittest.main()
