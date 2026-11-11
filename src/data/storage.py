"""Load and save records using JSON Lines storage."""

from pathlib import Path

import jsonlines


def load_records(file_path: Path) -> list[dict]:
    """Load records from a JSONL file.

    A missing or empty file returns an empty list.
    Invalid JSONL raises a readable ValueError.
    """
    if not file_path.exists():
        return []

    if file_path.stat().st_size == 0:
        return []

    try:
        with jsonlines.open(file_path, mode="r") as reader:
            return list(reader.iter(type=dict))
    except jsonlines.InvalidLineError as exc:
        raise ValueError(
            f"Record file is damaged at line {exc.lineno}."
        ) from exc
    except OSError as exc:
        raise ValueError(
            f"Unable to read record file: {exc}"
        ) from exc


def save_records(records: list[dict], file_path: Path) -> None:
    """Save all records to a JSONL file."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with jsonlines.open(file_path, mode="w") as writer:
            writer.write_all(records)
    except OSError as exc:
        raise ValueError(
            f"Unable to save record file: {exc}"
        ) from exc
