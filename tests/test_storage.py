"""Tests for JSONL record storage."""

import tempfile
import unittest
from pathlib import Path

from src.data.storage import load_records, save_records


class TestStorage(unittest.TestCase):

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "missing.jsonl"

            records = load_records(file_path)

            self.assertEqual(records, [])

    def test_empty_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "empty.jsonl"
            file_path.touch()

            records = load_records(file_path)

            self.assertEqual(records, [])

    def test_save_and_load_records(self):
        sample_records = [
            {
                "ID": 1,
                "Type": "client",
                "Name": "Test Client",
            },
            {
                "ID": 1,
                "Type": "airline",
                "Company Name": "Test Airline",
            },
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "records.jsonl"

            save_records(sample_records, file_path)
            loaded_records = load_records(file_path)

            self.assertEqual(loaded_records, sample_records)

    def test_damaged_file_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "damaged.jsonl"

            file_path.write_text(
                '{"ID": 1, "Type": "client"}\n'
                'this is not valid json\n',
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_records(file_path)


if __name__ == "__main__":
    unittest.main()
