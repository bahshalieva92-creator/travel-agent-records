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
