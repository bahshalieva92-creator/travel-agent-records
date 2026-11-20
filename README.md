# Travel Agent Record Management System

**University of Liverpool | MSc Data Science and Artificial Intelligence**

**Module:** Software Development in Practice  
**Group:** A  
**Submission deadline:** 23 November 2026, 23:59 UK time

## Project overview

This group project developed a Python desktop application for a specialist travel agent.

The application manages three types of records:

- **Clients:** Names, addresses and contact information.
- **Airlines:** Airline company information.
- **Flights:** Clients, airlines, dates and departure/arrival cities.

Users can create, search, display, update and delete records through a graphical user interface (GUI).

## Project status

**The application is complete and has been tested.**

The Clients, Airlines and Flights tabs are functional, including record-management operations, searching, validation and user-friendly messages. Records are saved and loaded using JSON Lines (JSONL).

## Requirements

- Python 3.14
- Tkinter (included with Python)
- Required Python dependencies, including JSON Lines support

## Running the application

The application can be launched using Python 3.14 or IDLE.

## Data storage

The application uses a list of dictionaries internally. Records are stored in a JSON Lines file, loaded on start-up and saved when the application closes normally.

## Testing

Automated testing uses Python's unittest framework. Testing evidence and requirements traceability are included in the group report.

## Collaboration

Group A developed the application using individual GitHub branches, commits, pull requests and peer reviews. GitHub Issues and the project board tracked actions and progress. The accompanying group report documents team roles, design decisions, testing and evaluation.

## Limitations

The application is an educational, single-user prototype. It uses local file storage without user authentication or encryption, and saves changes when closed normally rather than after every edit.
