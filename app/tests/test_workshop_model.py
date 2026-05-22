import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "api"))

from models.workshop import WorkshopPayload


VALID_PAYLOAD = {
    "title": "Workshop Example",
    "category": "Docker",
    "status": "draft",
    "difficulty": "fundamentals",
    "duration_hours": 4,
    "summary": "A valid summary that is long enough for the workshop payload validator.",
    "description": "This description is intentionally long enough to satisfy the validator.\nIt also uses multiple lines for readability.",
    "objectives": [
        "Explain the fundamentals cleanly.",
        "Ship a safe practice exercise."
    ],
    "stack": ["FastAPI", "Docker"],
    "published": False,
}


class WorkshopModelTests(unittest.TestCase):
    def test_valid_payload_parses(self):
        payload = WorkshopPayload(**VALID_PAYLOAD)
        self.assertEqual(payload.category, "Docker")
        self.assertEqual(len(payload.objectives), 2)

    def test_objectives_need_multiple_items(self):
        with self.assertRaises(ValueError):
            WorkshopPayload(
                **{
                    **VALID_PAYLOAD,
                    "objectives": ["Only one objective"],
                }
            )


if __name__ == "__main__":
    unittest.main()
