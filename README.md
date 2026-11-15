# Travel Agent Record Management System

**University of Liverpool | MSc Data Science and Artificial Intelligence**

**Module:** Software Development in Practice  
**Group:** A  
**Submission deadline:** 23 November 2026, 23:59 UK time

## Project overview

This group project develops a Python desktop application for a specialist travel agent.

The application is designed to manage three types of records:

- **Clients:** names, addresses and contact information.
- **Airlines:** airline company information.
- **Flights:** clients, airlines, dates and departure/arrival cities.

The application must support creating, searching, displaying, updating and deleting records through a graphical user interface (GUI).

## Current development status

The application is under development.

The Clients and Airlines interfaces currently display sample data and support selecting records and clearing forms.

Search and record-management operations are not yet connected to the underlying functions. The Flights interface is also being developed.

## Requirements

- Python 3.14
- GitHub Desktop
- Python IDLE or another suitable code editor
- The `jsonlines` package. Install it once from the project folder:
  - macOS: `python3.14 -m pip install -r requirements.txt`
  - Windows: `py -m pip install -r requirements.txt`

## Running the application

### Using IDLE

1. Open IDLE 3.14.
2. Select **File → Open**.
3. Navigate to `travel-agent-records/src/main.py`.
4. Select **Run → Run Module**, or press F5.

### Using Terminal (macOS)

From the root project folder:

```bash
python3.14 src/main.py
```

### Using Windows

From the root project folder:

```bash
py src\main.py
```

## Data storage

The assignment specifies a list of dictionaries as the internal record representation.

The agreed project design uses JSON Lines (`.jsonl`) for persistent storage, with the data file located at:

`src/record/record.jsonl`

The application must load existing records when it starts and save them when it closes.

## Running unit tests

From the root project folder, run:

```bash
python3.14 -m unittest discover -s tests
```

On Windows, use the corresponding Python 3.14 launcher.

Unit tests will be developed for the application's modules as implementation progresses.

## Project structure

```text
travel-agent-records/
├── docs/                 Project documentation and meeting minutes
├── src/
│   ├── conf/             Configuration
│   ├── data/             Storage functions
│   ├── gui/              Graphical user interface
│   ├── record/           Record-management logic and JSONL data
│   └── main.py           Application entry point
├── tests/                Unit tests
├── README.md             Project instructions
└── requirements.txt      Dependency information
```

## GitHub collaboration workflow

All team members work on individual development branches.

1. Fetch the latest repository changes before starting.
2. Create or switch to your working branch.
3. Develop and test changes locally.
4. Commit small, meaningful changes using the prescribed PyInstaller convention.
5. Push commits to GitHub.
6. Create a pull request.
7. Obtain peer review before merging into `main`.

Do not commit directly to `main`.

## Team responsibilities

See [Team Members and Responsibilities](docs/team.md) for the agreed role leads and collaborative working arrangements.

## Project reporting and submission

The group will maintain:

- Meeting minutes and action records.
- Development and testing evidence.
- A group report of no more than 1,000 words.
- A shared final repository containing the completed application.

All members must submit identical group work by the assignment deadline. Individual peer assessments are submitted separately.

## Known limitations

The application remains under development. GUI elements that are visible but not connected to record-management functions should not yet be treated as functional.

Further testing, integration and evaluation will be completed before final submission.
