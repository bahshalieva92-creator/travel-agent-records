"""Integration tests for record management and JSONL persistence."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src"),
)

from data.storage import load_records, save_records
from record.records import (
    create_record,
    delete_record,
    update_record,
)

class TestPersistenceIntegration(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_directory.name) / "records.jsonl"

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_created_record_survives_save_and_reload(self):
        records = []

        create_record(
            records,
            "client",
            {
                "Name": "Anna Schmidt",
                "Address Line 1": "1 Example Street",
                "City": "Liverpool",
                "Country": "UK",
                "Phone Number": "01234567890",
            },
        )

        save_records(records, self.file_path)
        reloaded_records = load_records(self.file_path)

        self.assertEqual(len(reloaded_records), 1)
        self.assertEqual(
            reloaded_records[0]["Name"],
            "Anna Schmidt",
        )

    def test_updated_record_survives_save_and_reload(self):
        records = []

        create_record(
            records,
            "airline",
            {
                "Company Name": "Example Airways",
            },
        )

        update_record(
            records,
            "airline",
            1,
            {
                "Company Name": "Updated Airways",
            },
        )

        save_records(records, self.file_path)
        reloaded_records = load_records(self.file_path)

        self.assertEqual(
            reloaded_records[0]["Company Name"],
            "Updated Airways",
        )

    def test_deleted_record_remains_deleted_after_reload(self):
        records = []

        create_record(
            records,
            "client",
            {
                "Name": "Anna Schmidt",
                "Address Line 1": "1 Example Street",
                "City": "Liverpool",
                "Country": "UK",
                "Phone Number": "01234567890",
            },
        )

        delete_record(
            records,
            "client",
            1,
        )

        save_records(records, self.file_path)
        reloaded_records = load_records(self.file_path)

        self.assertEqual(reloaded_records, [])

    def test_multiple_record_types_survive_reload(self):
        records = []

        create_record(
            records,
            "client",
            {
                "Name": "Anna Schmidt",
                "Address Line 1": "1 Example Street",
                "City": "Liverpool",
                "Country": "UK",
                "Phone Number": "01234567890",
            },
        )

        create_record(
            records,
            "airline",
            {
                "Company Name": "Example Airways",
            },
        )

        create_record(
            records,
            "flight",
            {
                "Client_ID": 1,
                "Airline_ID": 1,
                "Date": "2026-11-23 14:30",
                "Start City": "Liverpool",
                "End City": "Paris",
            },
        )

        save_records(records, self.file_path)
        reloaded_records = load_records(self.file_path)

        self.assertEqual(len(reloaded_records), 3)

        self.assertEqual(
            {record["Type"] for record in reloaded_records},
            {"client", "airline", "flight"},
        )


if __name__ == "__main__":
    unittest.main()
