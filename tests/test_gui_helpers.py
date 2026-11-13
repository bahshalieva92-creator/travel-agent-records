"""Unit tests for the helper functions in src/gui/app.py.

Covers the form checks and the flight date helpers without opening a
window. Run: python3 -m unittest discover -s tests
"""

import sys
import unittest
from datetime import datetime
from pathlib import Path

# Let the tests import the app's code from the src folder (see Issue #2)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from gui.app import (choice_name, city_choices, date_in_words, find_choice,
                     first_missing_field, make_choices, phone_is_valid,
                     read_entries, real_date, records_of_type)

# A few records of each type, used by the list and drop-down tests
TEST_RECORDS = [
    {"ID": 1, "Type": "client", "Name": "Anna Schmidt", "City": "Frankfurt"},
    {"ID": 10, "Type": "client", "Name": "Alejandro Hernández Gutiérrez",
     "City": "Mexico City"},
    {"ID": 2, "Type": "client", "Name": "Stella Cortner", "City": ""},
    {"ID": 13, "Type": "airline", "Company Name": "Lufthansa"},
    {"ID": 3, "Type": "flight", "Client_ID": 1, "Airline_ID": 13,
     "Date": "2026-11-20 07:45", "Start City": "Baku",
     "End City": "Istanbul"},
]


class FakeEntry:
    """Pretend entry box: get() returns the stored text."""

    def __init__(self, text):
        """Store the text the box holds."""
        self.text = text

    def get(self):
        """Return the stored text, like tkinter's Entry.get()."""
        return self.text


class TestFormChecks(unittest.TestCase):
    """Checks run by Create and Update on the Clients and Airlines tabs."""

    def test_read_entries_trims_spaces(self):
        """read_entries removes spaces before and after each value."""
        entries = {"Name": FakeEntry("  Anna Schmidt  "),
                   "City": FakeEntry("Frankfurt")}
        self.assertEqual(read_entries(entries),
                         {"Name": "Anna Schmidt", "City": "Frankfurt"})

    def test_first_missing_field_finds_the_first_empty_one(self):
        """first_missing_field returns the first empty field in form order."""
        values = {"Name": "Anna Schmidt", "Phone Number": "", "City": ""}
        self.assertEqual(
            first_missing_field(values, ["Name", "Phone Number", "City"]),
            "Phone Number")

    def test_first_missing_field_when_all_filled(self):
        """first_missing_field returns "" when nothing is missing."""
        values = {"Name": "Anna Schmidt", "City": "Frankfurt"}
        self.assertEqual(first_missing_field(values, ["Name", "City"]), "")

    def test_spaces_only_counts_as_missing(self):
        """A required field with only spaces counts as empty."""
        values = read_entries({"Company Name": FakeEntry("   ")})
        self.assertEqual(first_missing_field(values, ["Company Name"]),
                         "Company Name")

    def test_valid_phone_numbers(self):
        """phone_is_valid accepts digits with spaces, +, -, ( and )."""
        for phone in ["+49 69 1234 5678", "(614) 555-0142", "020 7946 0321"]:
            with self.subTest(phone=phone):
                self.assertTrue(phone_is_valid(phone))

    def test_invalid_phone_numbers(self):
        """phone_is_valid rejects letters, no digits and empty text."""
        for phone in ["abc", "+", "", "12a", "020 7946 0321 ext 5"]:
            with self.subTest(phone=phone):
                self.assertFalse(phone_is_valid(phone))


class TestFlightDates(unittest.TestCase):
    """Checks run by Create and Update on the Flights tab."""

    def test_real_date_returns_the_date_and_time(self):
        """real_date returns a datetime for a date that exists."""
        self.assertEqual(real_date(2026, 11, 20, 7, 45),
                         datetime(2026, 11, 20, 7, 45))

    def test_real_date_rejects_31_february(self):
        """real_date returns None for 31 February."""
        self.assertIsNone(real_date(2026, 2, 31, 12, 0))

    def test_real_date_knows_leap_years(self):
        """29 February exists in 2028 but not in 2027."""
        self.assertIsNotNone(real_date(2028, 2, 29, 12, 0))
        self.assertIsNone(real_date(2027, 2, 29, 12, 0))

    def test_date_in_words_has_no_leading_zero(self):
        """date_in_words writes 1 November 2026, not 01 November."""
        self.assertEqual(date_in_words(2026, 11, 1), "1 November 2026")

    def test_date_in_words_names_an_impossible_date(self):
        """date_in_words still writes 31 February 2026 for the message."""
        self.assertEqual(date_in_words(2026, 2, 31), "31 February 2026")


class TestListsAndChoices(unittest.TestCase):
    """Checks for the lists and drop-downs on the Flights tab."""

    def test_records_of_type_keeps_only_that_type(self):
        """records_of_type returns the clients and nothing else."""
        clients = records_of_type(TEST_RECORDS, "client")
        self.assertEqual([client["ID"] for client in clients], [1, 10, 2])

    def test_make_choices_sorts_by_name(self):
        """make_choices gives "ID – name" choices sorted A to Z by name."""
        choices = make_choices(records_of_type(TEST_RECORDS, "client"))
        self.assertEqual(choices, ["10 – Alejandro Hernández Gutiérrez",
                                   "1 – Anna Schmidt", "2 – Stella Cortner"])

    def test_find_choice_matches_the_whole_id(self):
        """find_choice finds ID 1 without mixing it up with ID 10."""
        choices = make_choices(records_of_type(TEST_RECORDS, "client"))
        self.assertEqual(find_choice(choices, 1), "1 – Anna Schmidt")
        self.assertEqual(find_choice(choices, 99), "")

    def test_choice_name_drops_the_id(self):
        """choice_name turns "13 – Lufthansa" into "Lufthansa"."""
        self.assertEqual(choice_name("13 – Lufthansa"), "Lufthansa")

    def test_city_choices_are_unique_sorted_and_not_blank(self):
        """city_choices lists every city once, A to Z, without blanks."""
        cities = city_choices(records_of_type(TEST_RECORDS, "client"),
                              records_of_type(TEST_RECORDS, "flight"))
        self.assertEqual(cities,
                         ["Baku", "Frankfurt", "Istanbul", "Mexico City"])


if __name__ == "__main__":
    unittest.main()
