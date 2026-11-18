"""Record-management logic for the travel agent application."""

from datetime import datetime

from conf.config import RECORD_TYPES, REQUIRED_FIELDS

def get_next_id(records: list[dict], record_type: str) -> int:
    """Return the next ID for a given record type."""
    if record_type not in RECORD_TYPES:
        raise ValueError(f"Unknown record type: {record_type}")

    existing_ids = [
        record["ID"]
        for record in records
        if record.get("Type") == record_type
        and isinstance(record.get("ID"), int)
    ]

    if not existing_ids:
        return 1

    return max(existing_ids) + 1

DATE_FORMAT = "%Y-%m-%d %H:%M"


def validate_required_fields(record_type: str, fields: dict) -> None:
    """Check that all required fields contain usable values."""
    if record_type not in RECORD_TYPES:
        raise ValueError(f"Unknown record type: {record_type}")

    for field_name in REQUIRED_FIELDS[record_type]:
        if field_name not in fields:
            raise ValueError(f"{field_name} is required.")

        value = fields[field_name]

        if isinstance(value, str) and not value.strip():
            raise ValueError(f"{field_name} is required.")

        if value is None:
            raise ValueError(f"{field_name} is required.")


def validate_date(date_text: str) -> None:
    """Check that a flight date uses YYYY-MM-DD HH:MM format."""
    try:
        datetime.strptime(date_text, DATE_FORMAT)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Date must use YYYY-MM-DD HH:MM format."
        ) from exc

def validate_flight_relationships(
    records: list[dict],
    fields: dict,
) -> None:
    """Check that a flight references an existing client and airline."""
    client_id = fields.get("Client_ID")
    airline_id = fields.get("Airline_ID")

    if not isinstance(client_id, int):
        raise ValueError("Client_ID must be an integer.")

    if not isinstance(airline_id, int):
        raise ValueError("Airline_ID must be an integer.")

    client_exists = any(
        record.get("Type") == "client"
        and record.get("ID") == client_id
        for record in records
    )

    if not client_exists:
        raise ValueError(
            f"Client_ID {client_id} does not match an existing client."
        )

    airline_exists = any(
        record.get("Type") == "airline"
        and record.get("ID") == airline_id
        for record in records
    )

    if not airline_exists:
        raise ValueError(
            f"Airline_ID {airline_id} does not match an existing airline."
        )


# The details that make two records of one type the same record
DUPLICATE_FIELDS = {
    "client": ("Name", "Phone Number"),
    "airline": ("Company Name",),
    "flight": ("Client_ID", "Airline_ID", "Date", "Start City", "End City"),
}


def validate_not_duplicate(
    records: list[dict],
    record_type: str,
    fields: dict,
    record_id: int | None = None,
) -> None:
    """Check that no other record of this type has the same details."""
    key_fields = DUPLICATE_FIELDS[record_type]

    def key(record: dict) -> list:
        # Ignore letter case and extra spaces in text
        return [
            " ".join(value.lower().split()) if isinstance(value, str)
            else value
            for value in (record.get(name) for name in key_fields)
        ]

    for record in records:
        if (
            record.get("Type") == record_type
            and record.get("ID") != record_id
            and key(record) == key(fields)
        ):
            raise ValueError(
                f"{record_type.capitalize()} ID {record['ID']} already has "
                f"the same {' and '.join(key_fields)}."
            )


def create_record(
    records: list[dict],
    record_type: str,
    fields: dict,
) -> dict:
    """Create, validate and append a new record."""
    if record_type not in RECORD_TYPES:
        raise ValueError(f"Unknown record type: {record_type}")

    validate_required_fields(record_type, fields)

    if record_type == "flight":
        validate_date(fields["Date"])
        validate_flight_relationships(records, fields)

    validate_not_duplicate(records, record_type, fields)

    new_record = {
        "ID": get_next_id(records, record_type),
        "Type": record_type,
        **fields,
    }

    records.append(new_record)

    return new_record

def search_records(
    records: list[dict],
    record_type: str,
    search_text: str,
) -> list[dict]:
    """Return records of one type that match the search text."""
    if record_type not in RECORD_TYPES:
        raise ValueError(f"Unknown record type: {record_type}")

    search_text = search_text.strip().lower()

    matching_records = []

    for record in records:
        if record.get("Type") != record_type:
            continue

        if not search_text:
            matching_records.append(record)
            continue

        for value in record.values():
            if search_text in str(value).lower():
                matching_records.append(record)
                break

    return matching_records

def update_record(
    records: list[dict],
    record_type: str,
    record_id: int,
    changed_fields: dict,
) -> dict:
    """Update an existing record after validating the proposed changes."""
    if record_type not in RECORD_TYPES:
        raise ValueError(f"Unknown record type: {record_type}")

    target_record = next(
        (
            record
            for record in records
            if record.get("Type") == record_type
            and record.get("ID") == record_id
        ),
        None,
    )

    if target_record is None:
        raise ValueError(
            f"{record_type.capitalize()} record with ID {record_id} not found."
        )

    updated_record = target_record.copy()

    for field_name, value in changed_fields.items():
        if field_name not in {"ID", "Type"}:
            updated_record[field_name] = value

    validate_required_fields(record_type, updated_record)

    if record_type == "flight":
        validate_date(updated_record["Date"])
        validate_flight_relationships(records, updated_record)

    validate_not_duplicate(records, record_type, updated_record, record_id)

    target_record.clear()
    target_record.update(updated_record)

    return target_record

def delete_record(
    records: list[dict],
    record_type: str,
    record_id: int,
) -> None:
    """Delete a record unless existing flights still reference it."""
    if record_type not in RECORD_TYPES:
        raise ValueError(f"Unknown record type: {record_type}")

    target_record = next(
        (
            record
            for record in records
            if record.get("Type") == record_type
            and record.get("ID") == record_id
        ),
        None,
    )

    if target_record is None:
        raise ValueError(
            f"{record_type.capitalize()} record with ID {record_id} not found."
        )

    if record_type == "client":
        linked_flights = [
            record
            for record in records
            if record.get("Type") == "flight"
            and record.get("Client_ID") == record_id
        ]

        if linked_flights:
            raise ValueError(
                f"Client ID {record_id} cannot be deleted because "
                f"{len(linked_flights)} flight(s) reference it."
            )

    if record_type == "airline":
        linked_flights = [
            record
            for record in records
            if record.get("Type") == "flight"
            and record.get("Airline_ID") == record_id
        ]

        if linked_flights:
            raise ValueError(
                f"Airline ID {record_id} cannot be deleted because "
                f"{len(linked_flights)} flight(s) reference it."
            )

    records.remove(target_record)
