import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CLIENTS_FILE = DATA_DIR / "clients.json"


def load_clients():
    """Load clients from the JSON file."""

    with open(CLIENTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)