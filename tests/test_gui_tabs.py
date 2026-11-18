"""GUI workflow tests: click through the real tabs of the app.

Each test opens the main window, invisible, with a temporary copy of the
45 sample records, so src/record/record.jsonl is never changed. The tests
are skipped on a computer without a screen.
Run: python3 -m unittest discover -s tests
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

# Let the tests import the app's code from the src folder (see Issue #2)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import tkinter as tk
from tkinter import ttk

from conf.config import DATA_FILE
from data.storage import load_records
from gui import app


def all_widgets(parent):
    """Give every widget inside parent, in the order they were made."""
    for child in parent.winfo_children():
        yield child
        yield from all_widgets(child)


class TestGuiTabs(unittest.TestCase):

    def setUp(self):
        # A copy of the sample records, so the real file is never changed
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.data_file = Path(folder.name) / "record.jsonl"
        shutil.copy(DATA_FILE, self.data_file)

        # Use the copy, and answer Yes to every question the app asks
        for patch in (mock.patch.object(app, "DATA_FILE", self.data_file),
                      mock.patch.object(app.messagebox, "askyesno",
                                        return_value=True),
                      mock.patch.object(app.messagebox, "showinfo"),
                      mock.patch.object(app.messagebox, "showerror")):
            patch.start()
            self.addCleanup(patch.stop)

        try:
            self.window = app.create_main_window()
        except tk.TclError as problem:
            self.skipTest("No screen for the GUI: " + str(problem))
        self.addCleanup(self.close_window)

        # Keep the window invisible while the tests click through it
        try:
            self.window.attributes("-alpha", 0.0)
        except tk.TclError:
            pass
        self.window.update()

        self.tab_bar = next(widget for widget in all_widgets(self.window)
                            if isinstance(widget, ttk.Notebook))
        self.tabs = {self.tab_bar.tab(tab, "text"): tab
                     for tab in self.tab_bar.winfo_children()}

    def close_window(self):
        """Close the window without saving, if a test has not closed it."""
        try:
            self.window.destroy()
        except tk.TclError:
            pass

    # Small helpers that act like the agent

    def open_tab(self, name):
        """Click a tab and give it back."""
        self.tab_bar.select(self.tabs[name])
        self.window.update()
        return self.tabs[name]

    def button(self, tab, text):
        """Find a button on a tab by its text."""
        return next(widget for widget in all_widgets(tab)
                    if isinstance(widget, ttk.Button)
                    and widget.cget("text") == text)

    def click(self, tab, text):
        """Click a button on a tab, like the agent would."""
        self.button(tab, text).invoke()
        self.window.update()

    def is_greyed_out(self, tab, text):
        """Give True if a button on a tab cannot be clicked."""
        return str(self.button(tab, text).cget("state")) == "disabled"

    def record_list(self, tab):
        """Find the list of records on a tab."""
        return next(widget for widget in all_widgets(tab)
                    if isinstance(widget, ttk.Treeview))

    def choose(self, tab, record_id):
        """Select a record in the list, like a click on its row."""
        self.record_list(tab).selection_set(str(record_id))
        self.window.update()

    def form(self, tab):
        """Give the form boxes on a tab by their label, without the *."""
        boxes = {}
        label = None
        for widget in all_widgets(tab):
            if isinstance(widget, ttk.Label):
                label = widget.cget("text").rstrip("*")
            elif type(widget) is ttk.Entry and label:
                boxes[label] = widget
                label = None
        return boxes

    def fill(self, tab, values):
        """Type values into the form boxes on a tab."""
        boxes = self.form(tab)
        for label, value in values.items():
            boxes[label].delete(0, "end")
            boxes[label].insert(0, value)

    def message(self, tab):
        """Give the message line at the bottom of a tab."""
        labels = [widget for widget in tab.winfo_children()
                  if isinstance(widget, ttk.Label)]
        return labels[-1].cget("text")

    def rows(self, tab):
        """Give the record IDs shown in the list on a tab."""
        return list(self.record_list(tab).get_children())

    def flight_boxes(self):
        """Give the Flights drop-downs and the five date and time boxes."""
        tab = self.tabs["Flights"]
        boxes = [widget for widget in all_widgets(tab)
                 if isinstance(widget, ttk.Combobox)]
        spins = [widget for widget in all_widgets(tab)
                 if isinstance(widget, ttk.Spinbox)]
        return boxes, spins

    def client_choices(self):
        """Give the clients offered in the Flights client drop-down."""
        boxes, spins = self.flight_boxes()
        return [str(choice) for choice in boxes[0].cget("values")]

    def new_client(self, name="Test Client", phone="+44 1904 000000"):
        """Fill in and create a new client on the Clients tab."""
        tab = self.open_tab("Clients")
        self.click(tab, "Clear")
        self.fill(tab, {"Name": name, "Phone Number": phone,
                        "Address Line 1": "1 Test Road", "City": "York",
                        "Country": "UK"})
        self.click(tab, "Create")
        return tab

    # The tests

    def test_clients_create_update_delete(self):
        tab = self.new_client()
        self.assertIn("16", self.rows(tab))
        self.assertIn("Test Client was added with ID 16.", self.message(tab))

        self.choose(tab, 16)
        self.fill(tab, {"City": "Leeds"})
        self.click(tab, "Update")
        self.assertIn("Leeds", self.record_list(tab).item("16", "values"))

        self.choose(tab, 16)
        self.click(tab, "Delete")
        self.assertNotIn("16", self.rows(tab))
        self.assertIn("was deleted", self.message(tab))

    def test_airlines_create_update_delete(self):
        tab = self.open_tab("Airlines")
        self.click(tab, "Clear")
        self.fill(tab, {"Company Name": "Test Air"})
        self.click(tab, "Create")
        self.assertIn("16", self.rows(tab))

        self.choose(tab, 16)
        self.fill(tab, {"Company Name": "Test Airways"})
        self.click(tab, "Update")
        self.assertIn("Test Airways",
                      self.record_list(tab).item("16", "values"))

        self.choose(tab, 16)
        self.click(tab, "Delete")
        self.assertNotIn("16", self.rows(tab))

    def test_flights_create_update_delete(self):
        tab = self.open_tab("Flights")
        self.click(tab, "Clear")
        boxes, spins = self.flight_boxes()
        client_box, from_box, to_box, airline_box = boxes[:4]
        client_box.set(client_box.cget("values")[0])
        airline_box.set(airline_box.cget("values")[0])
        from_box.set("London")
        to_box.set("Paris")
        for box, value in zip(spins, ["2027", "05", "10", "09", "30"]):
            box.set(value)
        self.click(tab, "Create")
        self.assertIn("16", self.rows(tab))
        self.assertIn("Flight 16 was added: ", self.message(tab))
        self.assertIn("London → Paris", self.message(tab))

        self.choose(tab, 16)
        to_box.set("Rome")
        self.click(tab, "Update")
        self.assertIn("Rome", self.record_list(tab).item("16", "values"))

        self.choose(tab, 16)
        self.click(tab, "Delete")
        self.assertNotIn("16", self.rows(tab))

    def test_missing_required_field_adds_nothing(self):
        tab = self.open_tab("Clients")
        self.click(tab, "Clear")
        self.fill(tab, {"Phone Number": "+44 1904 000000"})
        self.click(tab, "Create")
        self.assertEqual(len(self.rows(tab)), 15)
        self.assertIn("Name", self.message(tab))

    def test_create_is_greyed_out_while_record_selected(self):
        for name in ("Clients", "Airlines", "Flights"):
            with self.subTest(tab=name):
                tab = self.open_tab(name)
                self.choose(tab, 1)
                self.assertTrue(self.is_greyed_out(tab, "Create"))
                self.click(tab, "Create")
                self.assertEqual(len(self.rows(tab)), 15)
                self.click(tab, "Clear")
                self.assertFalse(self.is_greyed_out(tab, "Create"))

    def test_duplicate_client_is_rejected(self):
        tab = self.new_client()
        self.new_client()
        self.assertEqual(len(self.rows(tab)), 16)
        self.assertIn("✗", self.message(tab))
        self.assertIn("already has the same", self.message(tab))

    def test_client_with_flights_cannot_be_deleted(self):
        tab = self.open_tab("Clients")
        self.choose(tab, 1)
        self.click(tab, "Delete")
        self.assertIn("1", self.rows(tab))
        self.assertIn("cannot be deleted", self.message(tab))
        self.assertIn("Use Show flights", self.message(tab))

    def test_search_shows_only_matching_rows(self):
        tab = self.open_tab("Airlines")
        search_field = next(widget for widget in all_widgets(tab)
                            if type(widget) is ttk.Entry)
        search_field.insert(0, "Lufthansa")
        self.click(tab, "Search")
        self.assertEqual(self.rows(tab), ["13"])

        self.click(tab, "Show all")
        self.assertEqual(len(self.rows(tab)), 15)

    def test_search_that_hides_the_record_clears_the_form(self):
        for name, text in (("Clients", "Kenji"), ("Airlines", "Emirates"),
                           ("Flights", "Hanoi")):
            with self.subTest(tab=name):
                tab = self.open_tab(name)
                self.choose(tab, 1)
                search_field = next(widget for widget in all_widgets(tab)
                                    if type(widget) is ttk.Entry)
                search_field.delete(0, "end")
                search_field.insert(0, text)
                self.click(tab, "Search")
                self.assertNotIn("1", self.rows(tab))
                self.assertTrue(self.is_greyed_out(tab, "Update"))
                self.assertTrue(self.is_greyed_out(tab, "Delete"))

    def test_new_client_appears_in_flights_dropdown(self):
        self.open_tab("Flights")
        self.assertFalse(any("Test Client" in choice
                             for choice in self.client_choices()))
        self.new_client()
        self.open_tab("Flights")
        self.assertIn("16 – Test Client", self.client_choices())

    def test_deleted_client_leaves_flights_dropdown(self):
        tab = self.new_client()
        self.choose(tab, 16)
        self.click(tab, "Delete")
        self.open_tab("Flights")
        self.assertFalse(any("Test Client" in choice
                             for choice in self.client_choices()))

    def test_records_saved_when_window_closes(self):
        self.new_client(name="Saved Person")
        # Run what happens when the agent closes the window
        self.window.tk.call(self.window.protocol("WM_DELETE_WINDOW"))
        saved = load_records(self.data_file)
        self.assertEqual(len(saved), 46)
        self.assertTrue(any(record.get("Name") == "Saved Person"
                            and record["ID"] == 16 for record in saved))


if __name__ == "__main__":
    unittest.main()
