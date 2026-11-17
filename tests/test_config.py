"""Tests for shared configuration values."""

import sys
import unittest
from pathlib import Path

# Let the tests import the app's code from the src folder (see Issue #2)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from conf import config


class TestConfig(unittest.TestCase):

    def test_data_file_points_to_record_jsonl(self):
        self.assertTrue(
            config.DATA_FILE.as_posix().endswith("record/record.jsonl")
        )

    def test_record_types_are_exactly_the_supported_types(self):
        self.assertEqual(
            config.RECORD_TYPES,
            {"client", "airline", "flight"},
        )

    def test_each_record_type_has_required_fields(self):
        self.assertIn("Name", config.REQUIRED_FIELDS["client"])
        self.assertIn("Company Name", config.REQUIRED_FIELDS["airline"])
        self.assertIn("Client_ID", config.REQUIRED_FIELDS["flight"])


if __name__ == "__main__":
    unittest.main()
