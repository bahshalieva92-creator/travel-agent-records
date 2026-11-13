"""Unit tests for the form-check helpers in src/gui/app.py.

Tests read_entries, first_missing_field and phone_is_valid without
opening a window. Run: python3 -m unittest discover -s tests
"""

import sys
import unittest
from pathlib import Path

# Let the tests import the app's code from the src folder (see Issue #2)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from gui.app import first_missing_field, phone_is_valid, read_entries


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


if __name__ == "__main__":
    unittest.main()
