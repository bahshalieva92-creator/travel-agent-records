"""Tests for record-management logic."""

import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src"),
)

from record.records import (
    create_record,
    delete_record,
    get_next_id,
    search_records,
    update_record,
    validate_date,
    validate_flight_relationships,
    validate_not_duplicate,
    validate_required_fields,
)


class TestGetNextID(unittest.TestCase):

    def test_first_id_is_one(self):
        records = []

        next_id = get_next_id(records, "client")

        self.assertEqual(next_id, 1)

    def test_next_id_uses_highest_existing_id(self):
        records = [
            {"ID": 1, "Type": "client"},
            {"ID": 3, "Type": "client"},
            {"ID": 2, "Type": "client"},
        ]

        next_id = get_next_id(records, "client")

        self.assertEqual(next_id, 4)

    def test_ids_are_separate_by_record_type(self):
        records = [
            {"ID": 5, "Type": "client"},
            {"ID": 2, "Type": "airline"},
        ]

        self.assertEqual(get_next_id(records, "client"), 6)
        self.assertEqual(get_next_id(records, "airline"), 3)
        self.assertEqual(get_next_id(records, "flight"), 1)

    def test_unknown_record_type_raises_value_error(self):
        with self.assertRaises(ValueError):
            get_next_id([], "hotel")


if __name__ == "__main__":
    unittest.main()



class TestRequiredFieldValidation(unittest.TestCase):

    def test_valid_client_fields_pass(self):
        fields = {
            "Name": "Anna Schmidt",
            "Address Line 1": "1 Example Street",
            "City": "Liverpool",
            "Country": "UK",
            "Phone Number": "01234567890",
        }

        validate_required_fields("client", fields)

    def test_missing_required_field_raises_value_error(self):
        fields = {
            "Name": "Anna Schmidt",
            "Address Line 1": "1 Example Street",
            "City": "Liverpool",
            "Country": "UK",
        }

        with self.assertRaises(ValueError):
            validate_required_fields("client", fields)

    def test_blank_required_field_raises_value_error(self):
        fields = {
            "Name": "   ",
            "Address Line 1": "1 Example Street",
            "City": "Liverpool",
            "Country": "UK",
            "Phone Number": "01234567890",
        }

        with self.assertRaises(ValueError):
            validate_required_fields("client", fields)

    def test_optional_client_fields_may_be_empty(self):
        fields = {
            "Name": "Anna Schmidt",
            "Address Line 1": "1 Example Street",
            "Address Line 2": "",
            "Address Line 3": "",
            "City": "Liverpool",
            "State": "",
            "Zip Code": "",
            "Country": "UK",
            "Phone Number": "01234567890",
        }

        validate_required_fields("client", fields)


class TestDateValidation(unittest.TestCase):

    def test_valid_date_passes(self):
        validate_date("2026-11-23 14:30")

    def test_invalid_date_format_raises_value_error(self):
        with self.assertRaises(ValueError):
            validate_date("23/11/2026 14:30")

    def test_impossible_date_raises_value_error(self):
        with self.assertRaises(ValueError):
            validate_date("2026-02-30 14:30")


class TestFlightRelationshipValidation(unittest.TestCase):

    def setUp(self):
        self.records = [
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

    def test_valid_client_and_airline_ids_pass(self):
        fields = {
            "Client_ID": 1,
            "Airline_ID": 1,
        }

        validate_flight_relationships(self.records, fields)

    def test_missing_client_raises_value_error(self):
        fields = {
            "Client_ID": 99,
            "Airline_ID": 1,
        }

        with self.assertRaises(ValueError):
            validate_flight_relationships(self.records, fields)

    def test_missing_airline_raises_value_error(self):
        fields = {
            "Client_ID": 1,
            "Airline_ID": 99,
        }

        with self.assertRaises(ValueError):
            validate_flight_relationships(self.records, fields)

    def test_client_id_must_be_integer(self):
        fields = {
            "Client_ID": "1",
            "Airline_ID": 1,
        }

        with self.assertRaises(ValueError):
            validate_flight_relationships(self.records, fields)

    def test_airline_id_must_be_integer(self):
        fields = {
            "Client_ID": 1,
            "Airline_ID": "1",
        }

        with self.assertRaises(ValueError):
            validate_flight_relationships(self.records, fields)




class TestCreateRecord(unittest.TestCase):

    def test_create_client_adds_id_and_type(self):
        records = []

        fields = {
            "Name": "Anna Schmidt",
            "Address Line 1": "1 Example Street",
            "Address Line 2": "",
            "Address Line 3": "",
            "City": "Liverpool",
            "State": "",
            "Zip Code": "",
            "Country": "UK",
            "Phone Number": "01234567890",
        }

        new_record = create_record(records, "client", fields)

        self.assertEqual(new_record["ID"], 1)
        self.assertEqual(new_record["Type"], "client")
        self.assertEqual(new_record["Name"], "Anna Schmidt")
        self.assertEqual(records, [new_record])

    def test_create_airline_adds_record(self):
        records = []

        fields = {
            "Company Name": "Example Airways",
        }

        new_record = create_record(records, "airline", fields)

        self.assertEqual(new_record["ID"], 1)
        self.assertEqual(new_record["Type"], "airline")
        self.assertEqual(
            new_record["Company Name"],
            "Example Airways",
        )

    def test_create_flight_with_valid_links(self):
        records = [
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

        fields = {
            "Client_ID": 1,
            "Airline_ID": 1,
            "Date": "2026-11-23 14:30",
            "Start City": "Liverpool",
            "End City": "Paris",
        }

        new_record = create_record(records, "flight", fields)

        self.assertEqual(new_record["ID"], 1)
        self.assertEqual(new_record["Type"], "flight")
        self.assertEqual(new_record["Client_ID"], 1)
        self.assertEqual(new_record["Airline_ID"], 1)

    def test_invalid_client_is_not_added(self):
        records = []

        fields = {
            "Name": "",
            "Address Line 1": "1 Example Street",
            "City": "Liverpool",
            "Country": "UK",
            "Phone Number": "01234567890",
        }

        with self.assertRaises(ValueError):
            create_record(records, "client", fields)

        self.assertEqual(records, [])

    def test_invalid_flight_is_not_added(self):
        records = [
            {
                "ID": 1,
                "Type": "client",
                "Name": "Test Client",
            },
        ]

        fields = {
            "Client_ID": 1,
            "Airline_ID": 99,
            "Date": "2026-11-23 14:30",
            "Start City": "Liverpool",
            "End City": "Paris",
        }

        with self.assertRaises(ValueError):
            create_record(records, "flight", fields)

        self.assertEqual(len(records), 1)

class TestSearchRecords(unittest.TestCase):

    def setUp(self):
        self.records = [
            {
                "ID": 1,
                "Type": "client",
                "Name": "Anna Schmidt",
                "City": "Liverpool",
            },
            {
                "ID": 2,
                "Type": "client",
                "Name": "John Smith",
                "City": "London",
            },
            {
                "ID": 1,
                "Type": "airline",
                "Company Name": "Example Airways",
            },
        ]

    def test_search_client_by_name(self):
        results = search_records(
            self.records,
            "client",
            "Anna",
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["Name"], "Anna Schmidt")

    def test_search_is_case_insensitive(self):
        results = search_records(
            self.records,
            "client",
            "liverpool",
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["ID"], 1)

    def test_search_only_returns_selected_record_type(self):
        results = search_records(
            self.records,
            "client",
            "1",
        )

        self.assertEqual(
            all(record["Type"] == "client" for record in results),
            True,
        )

    def test_empty_search_returns_all_records_of_type(self):
        results = search_records(
            self.records,
            "client",
            "",
        )

        self.assertEqual(len(results), 2)

    def test_no_match_returns_empty_list(self):
        results = search_records(
            self.records,
            "client",
            "Manchester",
        )

        self.assertEqual(results, [])

    def test_unknown_record_type_raises_value_error(self):
        with self.assertRaises(ValueError):
            search_records(
                self.records,
                "hotel",
                "test",
            )

class TestUpdateRecord(unittest.TestCase):

    def setUp(self):
        self.records = [
            {
                "ID": 1,
                "Type": "client",
                "Name": "Anna Schmidt",
                "Address Line 1": "1 Example Street",
                "City": "Liverpool",
                "Country": "UK",
                "Phone Number": "01234567890",
            },
            {
                "ID": 1,
                "Type": "airline",
                "Company Name": "Example Airways",
            },
        ]

    def test_update_client_name(self):
        updated = update_record(
            self.records,
            "client",
            1,
            {"Name": "Anna Jones"},
        )

        self.assertEqual(updated["Name"], "Anna Jones")

    def test_update_preserves_id_and_type(self):
        updated = update_record(
            self.records,
            "client",
            1,
            {
                "ID": 99,
                "Type": "airline",
                "City": "London",
            },
        )

        self.assertEqual(updated["ID"], 1)
        self.assertEqual(updated["Type"], "client")
        self.assertEqual(updated["City"], "London")

    def test_missing_record_raises_value_error(self):
        with self.assertRaises(ValueError):
            update_record(
                self.records,
                "client",
                99,
                {"Name": "Missing"},
            )

    def test_invalid_required_field_is_rejected(self):
        with self.assertRaises(ValueError):
            update_record(
                self.records,
                "client",
                1,
                {"Name": "   "},
            )

        self.assertEqual(
            self.records[0]["Name"],
            "Anna Schmidt",
        )

    def test_valid_flight_update(self):
        records = [
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
            {
                "ID": 1,
                "Type": "flight",
                "Client_ID": 1,
                "Airline_ID": 1,
                "Date": "2026-11-23 14:30",
                "Start City": "Liverpool",
                "End City": "Paris",
            },
        ]

        updated = update_record(
            records,
            "flight",
            1,
            {"End City": "Madrid"},
        )

        self.assertEqual(updated["End City"], "Madrid")

    def test_invalid_flight_relationship_is_rejected(self):
        records = [
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
            {
                "ID": 1,
                "Type": "flight",
                "Client_ID": 1,
                "Airline_ID": 1,
                "Date": "2026-11-23 14:30",
                "Start City": "Liverpool",
                "End City": "Paris",
            },
        ]

        with self.assertRaises(ValueError):
            update_record(
                records,
                "flight",
                1,
                {"Airline_ID": 99},
            )

        self.assertEqual(records[2]["Airline_ID"], 1)

    def test_unknown_record_type_raises_value_error(self):
        with self.assertRaises(ValueError):
            update_record(
                self.records,
                "hotel",
                1,
                {"Name": "Example"},
            )

class TestDeleteRecord(unittest.TestCase):

    def setUp(self):
        self.records = [
            {
                "ID": 1,
                "Type": "client",
                "Name": "Anna Schmidt",
            },
            {
                "ID": 2,
                "Type": "client",
                "Name": "John Smith",
            },
            {
                "ID": 1,
                "Type": "airline",
                "Company Name": "Example Airways",
            },
        ]

    def test_delete_existing_client(self):
        delete_record(
            self.records,
            "client",
            1,
        )

        self.assertEqual(len(self.records), 2)

        self.assertFalse(
            any(
                record.get("Type") == "client"
                and record.get("ID") == 1
                for record in self.records
            )
        )

    def test_delete_only_target_record(self):
        delete_record(
            self.records,
            "client",
            1,
        )

        self.assertTrue(
            any(
                record.get("Type") == "client"
                and record.get("ID") == 2
                for record in self.records
            )
        )

        self.assertTrue(
            any(
                record.get("Type") == "airline"
                and record.get("ID") == 1
                for record in self.records
            )
        )

    def test_missing_record_raises_value_error(self):
        with self.assertRaises(ValueError):
            delete_record(
                self.records,
                "client",
                99,
            )

    def test_unknown_record_type_raises_value_error(self):
        with self.assertRaises(ValueError):
            delete_record(
                self.records,
                "hotel",
                1,
            )

    def test_failed_delete_does_not_change_records(self):
        original_records = self.records.copy()

        with self.assertRaises(ValueError):
            delete_record(
                self.records,
                "client",
                99,
            )

        self.assertEqual(
            self.records,
            original_records,
        )

class TestLinkedFlightDeletionProtection(unittest.TestCase):

    def setUp(self):
        self.records = [
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
            {
                "ID": 1,
                "Type": "flight",
                "Client_ID": 1,
                "Airline_ID": 1,
                "Date": "2026-11-23 14:30",
                "Start City": "Liverpool",
                "End City": "Paris",
            },
        ]

    def test_client_with_linked_flight_cannot_be_deleted(self):
        with self.assertRaises(ValueError):
            delete_record(
                self.records,
                "client",
                1,
            )

        self.assertTrue(
            any(
                record.get("Type") == "client"
                and record.get("ID") == 1
                for record in self.records
            )
        )

    def test_airline_with_linked_flight_cannot_be_deleted(self):
        with self.assertRaises(ValueError):
            delete_record(
                self.records,
                "airline",
                1,
            )

        self.assertTrue(
            any(
                record.get("Type") == "airline"
                and record.get("ID") == 1
                for record in self.records
            )
        )

    def test_flight_can_be_deleted(self):
        delete_record(
            self.records,
            "flight",
            1,
        )

        self.assertFalse(
            any(
                record.get("Type") == "flight"
                and record.get("ID") == 1
                for record in self.records
            )
        )

    def test_client_can_be_deleted_after_linked_flight_removed(self):
        delete_record(
            self.records,
            "flight",
            1,
        )

        delete_record(
            self.records,
            "client",
            1,
        )

        self.assertFalse(
            any(
                record.get("Type") == "client"
                and record.get("ID") == 1
                for record in self.records
            )
        )


class TestDuplicateRecords(unittest.TestCase):

    def setUp(self):
        self.client = {
            "Name": "Anna Schmidt",
            "Address Line 1": "1 Example Street",
            "City": "Liverpool",
            "Country": "UK",
            "Phone Number": "01234567890",
        }
        self.flight = {
            "Client_ID": 1,
            "Airline_ID": 1,
            "Date": "2026-12-05 14:30",
            "Start City": "Frankfurt",
            "End City": "London",
        }
        self.records = [
            {"ID": 1, "Type": "client", **self.client},
            {"ID": 1, "Type": "airline", "Company Name": "Lufthansa"},
            {"ID": 1, "Type": "flight", **self.flight},
        ]

    def test_same_client_is_not_added(self):
        with self.assertRaises(ValueError):
            create_record(self.records, "client", dict(self.client))

        self.assertEqual(len(self.records), 3)

    def test_case_and_spaces_are_ignored(self):
        fields = dict(self.client, Name="  anna   SCHMIDT ")

        with self.assertRaises(ValueError):
            create_record(self.records, "client", fields)

    def test_same_name_with_other_phone_is_added(self):
        fields = dict(self.client, **{"Phone Number": "09876543210"})

        new_record = create_record(self.records, "client", fields)

        self.assertEqual(new_record["ID"], 2)

    def test_same_airline_is_not_added(self):
        with self.assertRaises(ValueError):
            create_record(
                self.records,
                "airline",
                {"Company Name": "lufthansa"},
            )

    def test_same_flight_is_not_added(self):
        with self.assertRaises(ValueError):
            create_record(self.records, "flight", dict(self.flight))

        self.assertEqual(len(self.records), 3)

    def test_flight_on_another_date_is_added(self):
        fields = dict(self.flight, Date="2026-12-06 14:30")

        new_record = create_record(self.records, "flight", fields)

        self.assertEqual(new_record["ID"], 2)

    def test_update_without_changes_is_allowed(self):
        update_record(self.records, "client", 1, {"City": "Leeds"})

        self.assertEqual(self.records[0]["City"], "Leeds")

    def test_update_into_another_client_is_rejected(self):
        create_record(
            self.records,
            "client",
            dict(self.client, Name="Ben Jones"),
        )

        with self.assertRaises(ValueError):
            update_record(
                self.records,
                "client",
                2,
                {"Name": "Anna Schmidt"},
            )

        self.assertEqual(self.records[-1]["Name"], "Ben Jones")

    def test_record_is_not_compared_with_itself(self):
        validate_not_duplicate(self.records, "flight", self.flight, 1)
