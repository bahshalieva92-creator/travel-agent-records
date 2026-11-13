# Data Format and Design Decisions

**Status:** DRAFT – to be agreed at the team meeting on Saturday 14 November 2026.
The Project Manager changes this to **AGREED** once everyone has replied "agree".

This file is the shared agreement that lets everyone work in parallel.
If anything here needs to change, open a GitHub Issue first and tell the team.

---

## 1. Records

All records are kept in memory as one list of dictionaries, as the brief asks:
`records: list = [{}, {}]`. Field names are written **exactly** as in the brief,
including spaces and capital letters.

### Client record

| Field | Type | Required | Example |
|---|---|---|---|
| `ID` | int | automatic | `1` |
| `Type` | str | automatic | `"client"` |
| `Name` | str | yes | `"Anna Schmidt"` |
| `Address Line 1` | str | yes | `"Bergerstraße 12"` |
| `Address Line 2` | str | no | `""` |
| `Address Line 3` | str | no | `""` |
| `City` | str | yes | `"Frankfurt"` |
| `State` | str | no | `""` |
| `Zip Code` | str | no | `"60316"` |
| `Country` | str | yes | `"Germany"` |
| `Phone Number` | str | yes | `"+49 69 1234 5678"` |

### Airline record

| Field | Type | Required | Example |
|---|---|---|---|
| `ID` | int | automatic | `1` |
| `Type` | str | automatic | `"airline"` |
| `Company Name` | str | yes | `"Lufthansa"` |

### Flight record

| Field | Type | Required | Example |
|---|---|---|---|
| `ID` | int | automatic | `1` |
| `Type` | str | automatic | `"flight"` |
| `Client_ID` | int | yes | `1` |
| `Airline_ID` | int | yes | `13` |
| `Date` | str | yes | `"2026-12-05 14:30"` |
| `Start City` | str | yes | `"Frankfurt"` |
| `End City` | str | yes | `"London"` |

Notes on flights:
- The brief does not give flights an `ID` or `Type`. We add both, so that every
  record can be found, updated and deleted in the same way, and so that the three
  record types can share one file.
- `Date` is saved as text in the format `"YYYY-MM-DD HH:MM"` (24-hour clock),
  because JSON has no date type. It is checked with
  `datetime.strptime(value, "%Y-%m-%d %H:%M")`.
- `Client_ID` and `Airline_ID` must belong to an existing client and airline.

---

## 2. IDs

- Each record type has its own numbering, starting at 1.
- A new record gets the **highest ID of its type + 1** (or 1 if there are none).
- The ID is created by the program, never typed by the agent. The GUI shows it
  as a read-only box.

---

## 3. Storage

- All records are saved in one JSON Lines file: `src/record/record.jsonl`
  (one record per line, all three types together), using the `jsonlines`
  package from `requirements.txt`.
- **When the app starts**, it checks whether the file exists and loads it.
  A missing or empty file gives an empty list.
- **When the app closes**, all records are saved back to the file.
- Special letters such as ß, ə and ễ must survive saving and loading.

---

## 4. Shared functions

These are the functions the GUI will call. Programmers may adjust the details,
but please tell the team (and the GUI designer) in the pull request.

| File | Function | What it does |
|---|---|---|
| `src/data/storage.py` | `load_records(file_path)` | Returns the list of records, or `[]` if the file is missing or empty |
| `src/data/storage.py` | `save_records(records, file_path)` | Saves all records to the file |
| `src/record/records.py` | `create_record(records, new_record)` | Gives the record its ID, adds it to the list and returns it |
| `src/record/records.py` | `update_record(records, record_type, record_id, new_values)` | Changes the fields of one record and returns it |
| `src/record/records.py` | `delete_record(records, record_type, record_id)` | Removes one record from the list |
| `src/record/records.py` | `search_records(records, record_type, text)` | Returns the records of that type where any field contains the text (not case-sensitive); empty text returns all of them |

---

## 5. Errors and rules

- When something is wrong, a function raises `ValueError` with a short, clear
  message written for the travel agent, for example
  `ValueError("Name is required.")`. The GUI shows this message in its message
  line. Functions do not use `print()` or open their own windows.
- Required fields must not be empty (see the tables above).
- A flight's `Client_ID` and `Airline_ID` must exist.
- A client or airline that still has flights cannot be deleted. The message tells
  the agent to delete or change those flights first.
- A flight `Date` in the past is **not** an error: `records.py` accepts it, so a
  real past trip can still be recorded. The GUI warns and asks instead (see
  section 7).

---

## 6. Code conventions

- **Imports:** the app runs from `src/main.py` (lecturer's skeleton), so inside the
  app we import without `src.`, e.g. `from data.storage import load_records`.
  Test files add one line pointing to the `src` folder, then import the same way.
  See Issue #2.
- **Running the app:** open `src/main.py` in IDLE and press F5, or run
  `python3 src/main.py` (Windows: `py src\main.py`).
- **Tests:** one test file per module in `tests/`, named `test_<module>.py`.
  Run them all from the project folder with `python3 -m unittest discover -s tests`
  (Windows: `py -m unittest discover -s tests`).
- **Git:** never commit straight to `main`. Work on your own branch, open a pull
  request and get one review before merging.
- **Commit messages** follow the PyInstaller guidelines from the brief:
  `Prefix: Capital letter, present tense, full stop.` on the first line (under
  72 characters), an empty line, then 1–3 lines explaining why.

---

## 7. GUI design decisions

- One window with a tab per record type: Clients, Airlines, Flights.
- Every tab has the same layout: search bar at the top, list in the middle,
  details form below, then the buttons and a message line. Agents learn it once.
- The ID box is read-only, because IDs are given automatically.
- Create, Update and Clear sit together on the left; Delete is set apart on the
  right so it is not clicked by mistake.
- Clicking a row fills the form, ready to update. Clear empties the form, ready
  to add a new record.
- Update and Delete are greyed out until a record is selected, so they cannot be
  clicked by mistake (suggested in team feedback).
- A note under each form explains that * marks a required field (suggested in
  team feedback).
- A count under each list, e.g. "Showing 15 of 15 clients", tells the agent how
  many records are shown, especially after a search (suggested in team feedback).
- The message line always tells the agent what to do next or what just happened.
- Flights will use drop-down lists to choose the client and airline, so the agent
  does not have to remember ID numbers.
- **Past dates: warn and ask.** If a flight's date and time are before now,
  Create and Update ask "This flight is on 5 March 2026 at 14:30, which is in
  the past. Save it anyway?" with **No** pre-selected. No keeps the form open
  and shows "⚠ Not saved. Change the date or time and try again."; Yes saves
  the flight. A past date is usually a typing mistake but can be a real trip,
  so the agent decides rather than the program blocking it.
