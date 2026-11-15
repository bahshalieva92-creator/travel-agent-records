"""Shared configuration values for the record management system."""

from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = SRC_DIR / "record" / "record.jsonl"

CLIENT_TYPE = "client"
AIRLINE_TYPE = "airline"
FLIGHT_TYPE = "flight"

RECORD_TYPES = {
    CLIENT_TYPE,
    AIRLINE_TYPE,
    FLIGHT_TYPE,
}

CLIENT_REQUIRED_FIELDS = {
    "Name",
    "Address Line 1",
    "City",
    "Country",
    "Phone Number",
}

AIRLINE_REQUIRED_FIELDS = {
    "Company Name",
}

FLIGHT_REQUIRED_FIELDS = {
    "Client_ID",
    "Airline_ID",
    "Date",
    "Start City",
    "End City",
}

REQUIRED_FIELDS = {
    CLIENT_TYPE: CLIENT_REQUIRED_FIELDS,
    AIRLINE_TYPE: AIRLINE_REQUIRED_FIELDS,
    FLIGHT_TYPE: FLIGHT_REQUIRED_FIELDS,
}
