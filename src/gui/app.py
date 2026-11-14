"""This is the main window of the Travel Agent Record Manager app."""

import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from datetime import date, datetime

# Message colours. Each message also starts with a symbol (✓ success,
# ✗ error, ⚠ warning), so colour is never the only signal, which helps
# colour-blind agents.
SUCCESS_COLOUR = "#1e8e3e"
ERROR_COLOUR = "#d93025"
WARNING_COLOUR = "#b06000"

# Fields that must be filled in, as agreed in the decisions file
CLIENT_REQUIRED = ["Name", "Phone Number", "Address Line 1", "City",
                   "Country"]
AIRLINE_REQUIRED = ["Company Name"]
FLIGHT_REQUIRED = ["Client", "From", "To", "Airline"]

# These are 6 sample client details from my sketch plus 9 new random ones
# to try out before the team's load function is ready.
SAMPLE_CLIENTS = [
    {"ID": 1, "Type": "client", "Name": "Anna Schmidt",
     "Address Line 1": "Bergerstraße 12", "Address Line 2": "",
     "Address Line 3": "", "City": "Frankfurt", "State": "",
     "Zip Code": "", "Country": "Germany",
     "Phone Number": "+49 69 1234 5678"},
    {"ID": 2, "Type": "client", "Name": "Stella Cortner",
     "Address Line 1": "ul. Marszałkowska 84", "Address Line 2": "",
     "Address Line 3": "", "City": "Warsaw", "State": "",
     "Zip Code": "", "Country": "Poland",
     "Phone Number": "+48 22 123 45 67"},
    {"ID": 3, "Type": "client", "Name": "Patrick Walkman",
     "Address Line 1": "27 Elm Grove", "Address Line 2": "Islington",
     "Address Line 3": "", "City": "London", "State": "",
     "Zip Code": "N1 7QP", "Country": "UK",
     "Phone Number": "020 7946 0321"},
    {"ID": 4, "Type": "client", "Name": "Paul Jefferson",
     "Address Line 1": "1450 Maple Avenue", "Address Line 2": "",
     "Address Line 3": "", "City": "Columbus", "State": "",
     "Zip Code": "", "Country": "USA",
     "Phone Number": "(614) 555-0142"},
    {"ID": 5, "Type": "client", "Name": "Maria Rossi",
     "Address Line 1": "Via Garibaldi 8", "Address Line 2": "",
     "Address Line 3": "", "City": "Rome", "State": "",
     "Zip Code": "", "Country": "Italy",
     "Phone Number": "+39 06 1234 5678"},
    {"ID": 6, "Type": "client", "Name": "Kenji Tanaka",
     "Address Line 1": "Sakura Mansion, Room 503", "Address Line 2": "",
     "Address Line 3": "", "City": "Tokyo", "State": "",
     "Zip Code": "", "Country": "Japan",
     "Phone Number": "+81 3 1234 5678"},
    {"ID": 7, "Type": "client", "Name": "Emily Hargreaves",
     "Address Line 1": "14 Wellington Road", "Address Line 2": "Camden",
     "Address Line 3": "", "City": "London", "State": "",
     "Zip Code": "NW1 8AB", "Country": "UK",
     "Phone Number": "020 7946 0587"},
    {"ID": 8, "Type": "client", "Name": "Leyla Mammadova",
     "Address Line 1": "Nizami küçəsi 45", "Address Line 2": "",
     "Address Line 3": "", "City": "Baku", "State": "",
     "Zip Code": "AZ1000", "Country": "Azerbaijan",
     "Phone Number": "+994 12 345 67 89"},
    {"ID": 9, "Type": "client", "Name": "Li Wei",
     "Address Line 1": "88 Nanjing Road", "Address Line 2": "",
     "Address Line 3": "", "City": "Shanghai", "State": "",
     "Zip Code": "200001", "Country": "China",
     "Phone Number": "+86 21 1234 5678"},
    {"ID": 10, "Type": "client", "Name": "Alejandro Hernández Gutiérrez",
     "Address Line 1":
         "Avenida Paseo de la Reforma 2620, Piso 14, Oficina 1403",
     "Address Line 2": "Colonia Lomas Altas",
     "Address Line 3": "", "City": "Mexico City", "State": "CDMX",
     "Zip Code": "11950", "Country": "Mexico",
     "Phone Number": "+52 55 1234 5678"},
    {"ID": 11, "Type": "client", "Name": "Sanne de Vries",
     "Address Line 1": "Keizersgracht 215", "Address Line 2": "",
     "Address Line 3": "", "City": "Amsterdam", "State": "",
     "Zip Code": "1016 DV", "Country": "Netherlands",
     "Phone Number": "+31 20 123 4567"},
    {"ID": 12, "Type": "client", "Name": "Nguyễn Thị Lan",
     "Address Line 1": "25 Hàng Bài Street",
     "Address Line 2": "Hoàn Kiếm District",
     "Address Line 3": "", "City": "Hanoi", "State": "",
     "Zip Code": "", "Country": "Vietnam",
     "Phone Number": "+84 24 1234 5678"},
    {"ID": 13, "Type": "client", "Name": "Tan Wei Ming",
     "Address Line 1": "Blk 123 Ang Mo Kio Avenue 3, #08-1234",
     "Address Line 2": "", "Address Line 3": "",
     "City": "Singapore", "State": "",
     "Zip Code": "560123", "Country": "Singapore",
     "Phone Number": "+65 6123 4567"},
    {"ID": 14, "Type": "client", "Name": "Ivan Petrov",
     "Address Line 1": "ul. Tverskaya 7", "Address Line 2": "",
     "Address Line 3": "", "City": "Moscow", "State": "",
     "Zip Code": "125009", "Country": "Russia",
     "Phone Number": "+7 495 123 45 67"},
    {"ID": 15, "Type": "client", "Name": "Olga Smirnova",
     "Address Line 1": "Nevsky Prospekt 28",
     "Address Line 2": "Apartment 14",
     "Address Line 3": "Entrance 2, Floor 4",
     "City": "Saint Petersburg", "State": "",
     "Zip Code": "191186", "Country": "Russia",
     "Phone Number": "+7 812 123 45 67"},
]

# These are 6 sample airlines from my sketch plus 9
# more from my clients' countries to try out
SAMPLE_AIRLINES = [
    {"ID": 1, "Type": "airline", "Company Name": "Aeroflot"},
    {"ID": 2, "Type": "airline", "Company Name": "Turkish Airlines"},
    {"ID": 3, "Type": "airline", "Company Name": "Qatar Airways"},
    {"ID": 4, "Type": "airline", "Company Name": "Spring Airlines"},
    {"ID": 5, "Type": "airline", "Company Name": "China Eastern Airlines"},
    {"ID": 6, "Type": "airline", "Company Name": "Emirates"},
    {"ID": 7, "Type": "airline", "Company Name": "China Southern Airlines"},
    {"ID": 8, "Type": "airline", "Company Name": "KLM Royal Dutch Airlines"},
    {"ID": 9, "Type": "airline", "Company Name": "Aerolíneas Argentinas"},
    {"ID": 10, "Type": "airline", "Company Name": "Aeroméxico"},
    {"ID": 11, "Type": "airline", "Company Name": "Azerbaijan Airlines"},
    {"ID": 12, "Type": "airline", "Company Name": "British Airways"},
    {"ID": 13, "Type": "airline", "Company Name": "Lufthansa"},
    {"ID": 14, "Type": "airline", "Company Name": "Singapore Airlines"},
    {"ID": 15, "Type": "airline", "Company Name": "Vietnam Airlines"},
]


# 15 sample flights that use my sample clients and airlines, to try
# out the Flights tab before the team's load function is ready.
SAMPLE_FLIGHTS = [
    {"ID": 1, "Type": "flight", "Client_ID": 1, "Airline_ID": 13,
     "Date": "2026-12-05 14:30", "Start City": "Frankfurt",
     "End City": "London"},
    {"ID": 2, "Type": "flight", "Client_ID": 1, "Airline_ID": 12,
     "Date": "2026-12-12 09:15", "Start City": "London",
     "End City": "Frankfurt"},
    {"ID": 3, "Type": "flight", "Client_ID": 8, "Airline_ID": 11,
     "Date": "2026-11-20 07:45", "Start City": "Baku",
     "End City": "Istanbul"},
    {"ID": 4, "Type": "flight", "Client_ID": 12, "Airline_ID": 15,
     "Date": "2026-11-28 23:10", "Start City": "Hanoi",
     "End City": "Ho Chi Minh City"},
    {"ID": 5, "Type": "flight", "Client_ID": 10, "Airline_ID": 9,
     "Date": "2027-01-08 06:00", "Start City": "Mexico City",
     "End City": "Buenos Aires"},
    {"ID": 6, "Type": "flight", "Client_ID": 6, "Airline_ID": 6,
     "Date": "2026-12-18 22:05", "Start City": "Tokyo",
     "End City": "Dubai"},
    {"ID": 7, "Type": "flight", "Client_ID": 9, "Airline_ID": 5,
     "Date": "2026-10-30 08:20", "Start City": "Shanghai",
     "End City": "Singapore"},
    {"ID": 8, "Type": "flight", "Client_ID": 13, "Airline_ID": 14,
     "Date": "2026-12-01 13:40", "Start City": "Singapore",
     "End City": "Tokyo"},
    {"ID": 9, "Type": "flight", "Client_ID": 14, "Airline_ID": 1,
     "Date": "2026-11-15 18:25", "Start City": "Moscow",
     "End City": "Saint Petersburg"},
    {"ID": 10, "Type": "flight", "Client_ID": 15, "Airline_ID": 2,
     "Date": "2026-12-22 11:00", "Start City": "Saint Petersburg",
     "End City": "Istanbul"},
    {"ID": 11, "Type": "flight", "Client_ID": 11, "Airline_ID": 8,
     "Date": "2027-02-14 10:30", "Start City": "Amsterdam",
     "End City": "Mexico City"},
    {"ID": 12, "Type": "flight", "Client_ID": 5, "Airline_ID": 3,
     "Date": "2026-10-25 16:50", "Start City": "Rome",
     "End City": "Doha"},
    {"ID": 13, "Type": "flight", "Client_ID": 4, "Airline_ID": 10,
     "Date": "2027-03-03 07:15", "Start City": "Columbus",
     "End City": "Mexico City"},
    {"ID": 14, "Type": "flight", "Client_ID": 7, "Airline_ID": 12,
     "Date": "2026-11-12 19:30", "Start City": "London",
     "End City": "Rome"},
    {"ID": 15, "Type": "flight", "Client_ID": 2, "Airline_ID": 4,
     "Date": "2027-01-20 12:00", "Start City": "Warsaw",
     "End City": "Shanghai"},
]


def show_message(message_label, text, kind="info"):
    """Show a message: ✓ success in green, ✗ error in red, ⚠ warning."""
    if kind == "success":
        message_label.config(text="✓ " + text, foreground=SUCCESS_COLOUR)
    elif kind == "error":
        message_label.config(text="✗ " + text, foreground=ERROR_COLOUR)
    elif kind == "warning":
        message_label.config(text="⚠ " + text, foreground=WARNING_COLOUR)
    else:
        message_label.config(text=text, foreground="")


def read_entries(entries):
    """Read every box in a form, with spaces trimmed from both ends."""
    values = {}
    for field, entry in entries.items():
        values[field] = entry.get().strip()
    return values


def first_missing_field(values, required_fields):
    """Give the first required field that is empty, or "" if none is."""
    for field in required_fields:
        if values[field] == "":
            return field
    return ""


def phone_is_valid(phone):
    """Check a phone number has digits and only digits, spaces, + - ( )."""
    has_digit = False
    for character in phone:
        if character.isdigit():
            has_digit = True
        elif character not in " +-()":
            return False
    return has_digit


def real_date(year, month, day, hour, minute):
    """Give the date and time, or None if the date does not exist."""
    try:
        return datetime(year, month, day, hour, minute)
    except ValueError:
        return None


def date_in_words(year, month, day):
    """Write a date the way people say it, for example 11 November 2026."""
    month_name = date(year, month, 1).strftime("%B")
    return str(day) + " " + month_name + " " + str(year)


def confirm_delete(parent, name):
    """Ask before deleting, with No as default, as it cannot be undone."""
    return messagebox.askyesno("Delete record",
                               "Delete " + name + "? This can't be "
                               "undone.", icon="warning",
                               default="no", parent=parent)


def confirm_discard(parent, name):
    """Ask before throwing away unsaved changes, with No as default."""
    return messagebox.askyesno("Unsaved changes",
                               "Discard your changes to " + name + "?",
                               icon="warning", default="no", parent=parent)


def reselect_row(record_list, record_id):
    """Select the row of the record in the form again, or no row at all."""
    if record_id and record_list.exists(record_id):
        record_list.selection_set(record_id)
    else:
        record_list.selection_remove(record_list.selection())


def text_found(values, text):
    """Check if the text is in any of the values, ignoring capitals."""
    for value in values:
        if text.lower() in str(value).lower():
            return True
    return False


def keep_matching_rows(record_list, text):
    """Remove the rows of a list that do not have the text in any column."""
    for row in record_list.get_children():
        if not text_found(record_list.item(row, "values"), text):
            record_list.delete(row)


def show_search_result(message_label, record_list, kind, text):
    """Tell the agent what the search found, or that nothing matches."""
    if not record_list.get_children():
        show_message(message_label, "No " + kind + " match '" + text + "'.",
                     "warning")
    elif text:
        show_message(message_label, "Showing " + kind + " that match '" +
                     text + "'.")
    else:
        show_message(message_label, "Showing all " + kind + ".")


def records_of_type(records, record_type):
    """Give only the records of one type, for example all the clients."""
    chosen = []
    for record in records:
        if record["Type"] == record_type:
            chosen.append(record)
    return chosen


def show_clients(client_list, clients):
    """Show each client as a separate new row in the list."""
    for client in clients:
        client_list.insert("", "end", iid=client["ID"], values=(
            client["ID"], client["Name"], client["Address Line 1"],
            client["Phone Number"], client["City"], client["Country"]))
        

def show_airlines(airline_list, airlines):
    """Show each airline as a separate new row in the list."""
    for airline in airlines:
        airline_list.insert("", "end", iid=airline["ID"], values=(
            airline["ID"], airline["Company Name"]))


def flight_date(flight):
    """Give the date of a flight, so flights can be sorted by date."""
    return flight["Date"]


def record_name(record):
    """Give the name of a client or airline, so they can be sorted."""
    if record["Type"] == "airline":
        return record["Company Name"]
    return record["Name"]


def make_choices(records):
    """Make the "ID – name" choices for a drop-down list, sorted by name."""
    choices = []
    for record in sorted(records, key=record_name):
        choices.append(str(record["ID"]) + " – " + record_name(record))
    return choices


def find_choice(choices, record_id):
    """Find the "ID – name" choice for this ID, or "" if there is none."""
    start = str(record_id) + " – "
    for choice in choices:
        if choice.startswith(start):
            return choice
    return ""


def choice_name(choice):
    """Give the name part of an "ID – name" choice."""
    return choice.split(" – ", 1)[-1]


def city_choices(clients, flights):
    """Make the city suggestions: every city already used, sorted A-Z."""
    cities = set()
    for client in clients:
        cities.add(client["City"])
    for flight in flights:
        cities.add(flight["Start City"])
        cities.add(flight["End City"])
    cities.discard("")
    return sorted(cities)


def show_flights(flight_list, flights, clients, airlines):
    """Show each flight as a row, soonest first, with names not IDs."""
    client_names = {}
    for client in clients:
        client_names[client["ID"]] = client["Name"]
    airline_names = {}
    for airline in airlines:
        airline_names[airline["ID"]] = airline["Company Name"]

    for flight in sorted(flights, key=flight_date):
        client_id = flight["Client_ID"]
        airline_id = flight["Airline_ID"]
        client_text = "Client not found (ID " + str(client_id) + ")"
        airline_text = "Airline not found (ID " + str(airline_id) + ")"
        flight_list.insert("", "end", iid=flight["ID"], values=(
            flight["ID"], flight["Date"],
            client_names.get(client_id, client_text),
            airline_names.get(airline_id, airline_text),
            flight["Start City"], flight["End City"]))


def create_clients_tab(clients_tab, records):
    """Create the Clients tab: search bar, list, form, buttons, message."""

    # Search bar with Search and Show all buttons
    search_bar = ttk.Frame(clients_tab)
    search_bar.pack(fill="x", padx=10, pady=10)

    search_title = ttk.Label(search_bar, text="Search clients:")
    search_title.pack(side="left")

    search_field = ttk.Entry(search_bar, width=40)
    search_field.pack(side="left", padx=5)

    search_button = ttk.Button(search_bar, text="Search")
    search_button.pack(side="left")

    show_all_button = ttk.Button(search_bar, text="Show all")
    show_all_button.pack(side="left", padx=5)

    # Clients list with the same 6 columns as my sketch:
    # ID, Name, Address, Phone number, City, Country
    # A frame holds the list and its scrollbar side by side
    list_frame = ttk.Frame(clients_tab)
    list_frame.pack(fill="both", expand=True, padx=10)
    
    columns = ("id", "name", "address", "phone", "city", "country")
    client_list = ttk.Treeview(list_frame, columns=columns,
                               show="headings", height=10)

    client_list.heading("id", text="ID")
    client_list.heading("name", text="Name")
    client_list.heading("address", text="Address Line 1")
    client_list.heading("phone", text="Phone Number")
    client_list.heading("city", text="City")
    client_list.heading("country", text="Country")

    client_list.column("id", width=55, stretch=False)
    client_list.column("name", width=140)
    client_list.column("address", width=180)
    client_list.column("phone", width=90)
    client_list.column("city", width=70)
    client_list.column("country", width=70)

    # Scrollbar, so that every client can be chosen
    list_scrollbar = ttk.Scrollbar(list_frame, orient="vertical",
                                   command=client_list.yview)
    list_scrollbar.pack(side="right", fill="y")
    client_list.configure(yscrollcommand=list_scrollbar.set)

    client_list.pack(side="left", fill="both", expand=True)
    show_clients(client_list, records_of_type(records, "client"))

    # Count under the list, so the agent knows how many clients are shown
    count_label = ttk.Label(clients_tab)
    count_label.pack(anchor="w", padx=10)

    def update_count():
        """Show how many clients are in the list right now."""
        shown = len(client_list.get_children())
        total = len(records_of_type(records, "client"))
        count_label.config(text="Showing " + str(shown) + " of " +
                                str(total) + " clients")

    update_count()

    # Client Details form from my sketch
    client_form = ttk.LabelFrame(clients_tab, text="Client Details")
    client_form.pack(fill="x", padx=10, pady=10)

    # Each field: (field name, label text, row, column).
    # Order improved from my original sketch order.
    form_fields = [
        ("ID", "ID (automatic)", 0, 0),
        ("Name", "Name*", 1, 0),
        ("Phone Number", "Phone Number*", 2, 0),
        ("Address Line 1", "Address Line 1*", 3, 0),
        ("Address Line 2", "Address Line 2", 4, 0),
        ("Address Line 3", "Address Line 3", 0, 2),
        ("City", "City*", 1, 2),
        ("State", "State", 2, 2),
        ("Zip Code", "Zip Code", 3, 2),
        ("Country", "Country*", 4, 2),
    ]
    
    client_entries = {}
    for field, text, row, column in form_fields:
        label = ttk.Label(client_form, text=text)
        label.grid(row=row, column=column, padx=5, pady=3, sticky="w")
        entry = ttk.Entry(client_form, width=30)
        entry.grid(row=row, column=column + 1, padx=5, pady=3)
        client_entries[field] = entry

    # The ID is shown automatically, so the agent cannot type it
    client_entries["ID"].config(state="readonly")

    # Note that explains the stars on the labels
    required_note = ttk.Label(client_form,
                              text="Fields marked * are required.")
    required_note.grid(row=5, column=0, columnspan=4, padx=5, pady=3,
                       sticky="w")

    # The form as it was last filled or cleared, to spot unsaved changes
    saved_form = {}

    def remember_form():
        """Remember the form as it is now, to compare with it later."""
        saved_form.clear()
        saved_form.update(read_entries(client_entries))

    def ok_to_leave_form():
        """Give True if nothing is unsaved, or the agent discards it."""
        if read_entries(client_entries) == saved_form:
            return True
        if client_entries["ID"].get():
            name = saved_form["Name"]
        else:
            name = "the new client"
        return confirm_discard(clients_tab, name)

    def clear_form():
        """Clear every box in the form."""
        if not ok_to_leave_form():
            return
        for entry in client_entries.values():
            entry.config(state="normal")
            entry.delete(0, "end")
        client_entries["ID"].config(state="readonly")
        update_button.config(state="disabled")
        delete_button.config(state="disabled")
        show_message(message_label, "Form cleared. Fill in the details "
                                    "to add a new client.")
        client_list.selection_remove(client_list.selection())
        remember_form()
        
    def fill_form(event):
        """Show the details of the chosen client in the form."""
        selected = client_list.selection()
        if not selected:
            return
        # The client already in the form: nothing to change
        if selected[0] == client_entries["ID"].get():
            return
        if not ok_to_leave_form():
            reselect_row(client_list, client_entries["ID"].get())
            return
        client_id = int(selected[0])
        for client in records_of_type(records, "client"):
            if client["ID"] == client_id:
                for field, entry in client_entries.items():
                    entry.config(state="normal")
                    entry.delete(0, "end")
                    entry.insert(0, client[field])
                client_entries["ID"].config(state="readonly")
                update_button.config(state="normal")
                delete_button.config(state="normal")
                show_message(message_label, "Showing " + client["Name"] +
                             ". Update details and click Update.")
                remember_form()

    client_list.bind("<<TreeviewSelect>>", fill_form)

    def check_form():
        """Check the form and point to the first problem, if any."""
        values = read_entries(client_entries)
        missing = first_missing_field(values, CLIENT_REQUIRED)
        if missing:
            show_message(message_label, missing + " is required.", "error")
            client_entries[missing].focus_set()
            return False
        if not phone_is_valid(values["Phone Number"]):
            show_message(message_label, "Phone Number can only have digits, "
                         "spaces and + - ( ).", "error")
            client_entries["Phone Number"].focus_set()
            return False
        return True

    def create_client():
        """Check the form, then add it as a new client."""
        if check_form():
            # To connect: create_record(records, new_client) from records.py
            show_message(message_label, "The details are valid. Saving will "
                         "work once the record functions are connected.",
                         "success")

    def update_client():
        """Check the form, then save the changes to the chosen client."""
        if check_form():
            # To connect: update_record(records, "client", ID, new_values)
            show_message(message_label, "The details are valid. Saving will "
                         "work once the record functions are connected.",
                         "success")

    def delete_client():
        """Ask first, then delete the chosen client."""
        selected = client_list.selection()
        if not selected:
            return
        values = client_list.item(selected[0], "values")
        name = values[1]
        if confirm_delete(clients_tab, name):
            # To connect: delete_record(records, "client", ID) from records.py
            show_message(message_label, "Delete confirmed. Deleting will "
                         "work once the record functions are connected.",
                         "success")
        else:
            show_message(message_label, name + " was not deleted.")

    # Buttons from my sketch: Delete set apart on the right
    button_bar = ttk.Frame(clients_tab)
    button_bar.pack(fill="x", padx=10)

    create_button = ttk.Button(button_bar, text="Create",
                               command=create_client)
    create_button.pack(side="left", padx=5)
    update_button = ttk.Button(button_bar, text="Update",
                               command=update_client)
    update_button.pack(side="left", padx=5)
    clear_button = ttk.Button(button_bar, text="Clear", command=clear_form)
    clear_button.pack(side="left", padx=5)
    delete_button = ttk.Button(button_bar, text="Delete",
                               command=delete_client)
    delete_button.pack(side="right", padx=5)

    # Update and Delete stay greyed out until a record is selected
    update_button.config(state="disabled")
    delete_button.config(state="disabled")

    # Message line shows the agent what happened or what to do
    message_label = ttk.Label(
        clients_tab,
        text="Select a client from the list, or fill in the form to add one.")
    message_label.pack(anchor="w", padx=10, pady=10)

    # Search: the Search button, Enter and every key typed filter the list
    def run_search(event=None):
        """Show only the clients with the search text in any column."""
        text = search_field.get().strip()
        for row in client_list.get_children():
            client_list.delete(row)
        show_clients(client_list, records_of_type(records, "client"))
        keep_matching_rows(client_list, text)
        update_count()
        reselect_row(client_list, client_entries["ID"].get())
        show_search_result(message_label, client_list, "clients", text)

    search_button.config(command=run_search)
    search_field.bind("<KeyRelease>", run_search)

    # Show all and the Esc key empty the search box and show every client
    def show_all(event=None):
        """Empty the search box and show every client again."""
        search_field.delete(0, "end")
        run_search()

    show_all_button.config(command=show_all)
    search_field.bind("<Escape>", show_all)

    # Remember the starting form, so changes can be spotted
    remember_form()

    # Give back the check, so the window can use it when closing
    return ok_to_leave_form
    

def create_airlines_tab(airlines_tab, records):
    """Create the Airlines tab: search bar, list, form, buttons, message."""

    # Search bar with Search and Show all buttons, same as on Clients
    search_bar = ttk.Frame(airlines_tab)
    search_bar.pack(fill="x", padx=10, pady=10)

    search_title = ttk.Label(search_bar, text="Search airlines:")
    search_title.pack(side="left")

    search_field = ttk.Entry(search_bar, width=40)
    search_field.pack(side="left", padx=5)

    search_button = ttk.Button(search_bar, text="Search")
    search_button.pack(side="left")

    show_all_button = ttk.Button(search_bar, text="Show all")
    show_all_button.pack(side="left", padx=5)

    # Airline list with 2 columns: ID and Company Name
    list_frame = ttk.Frame(airlines_tab)
    list_frame.pack(fill="both", expand=True, padx=10)

    columns = ("id", "company")
    airline_list = ttk.Treeview(list_frame, columns=columns,
                                show="headings", height=10)

    airline_list.heading("id", text="ID")
    airline_list.heading("company", text="Company Name")

    airline_list.column("id", width=55, stretch=False)
    airline_list.column("company", width=300)

    # Scrollbar, so every airline can be reached
    list_scrollbar = ttk.Scrollbar(list_frame, orient="vertical",
                                   command=airline_list.yview)
    list_scrollbar.pack(side="right", fill="y")
    airline_list.configure(yscrollcommand=list_scrollbar.set)

    airline_list.pack(side="left", fill="both", expand=True)
    show_airlines(airline_list, records_of_type(records, "airline"))

    # Count under the list, so the agent knows how many airlines are shown
    count_label = ttk.Label(airlines_tab)
    count_label.pack(anchor="w", padx=10)

    def update_count():
        """Show how many airlines are in the list right now."""
        shown = len(airline_list.get_children())
        total = len(records_of_type(records, "airline"))
        count_label.config(text="Showing " + str(shown) + " of " +
                                str(total) + " airlines")

    update_count()

    # Airline Details form, same style as Client Details
    airline_form = ttk.LabelFrame(airlines_tab, text="Airline Details")
    airline_form.pack(fill="x", padx=10, pady=10)

    # Each field contains field name, label text, row, column
    form_fields = [
        ("ID", "ID (automatic)", 0, 0),
        ("Company Name", "Company Name*", 1, 0),
    ]

    airline_entries = {}
    for field, text, row, column in form_fields:
        label = ttk.Label(airline_form, text=text)
        label.grid(row=row, column=column, padx=5, pady=3, sticky="w")
        entry = ttk.Entry(airline_form, width=30)
        entry.grid(row=row, column=column + 1, padx=5, pady=3)
        airline_entries[field] = entry

    # The ID is shown automatically, so the agent cannot type it
    airline_entries["ID"].config(state="readonly")

    # Note that explains the stars on the labels
    required_note = ttk.Label(airline_form,
                              text="Fields marked * are required.")
    required_note.grid(row=2, column=0, columnspan=4, padx=5, pady=3,
                       sticky="w")

    # The form as it was last filled or cleared, to spot unsaved changes
    saved_form = {}

    def remember_form():
        """Remember the form as it is now, to compare with it later."""
        saved_form.clear()
        saved_form.update(read_entries(airline_entries))

    def ok_to_leave_form():
        """Give True if nothing is unsaved, or the agent discards it."""
        if read_entries(airline_entries) == saved_form:
            return True
        if airline_entries["ID"].get():
            name = saved_form["Company Name"]
        else:
            name = "the new airline"
        return confirm_discard(airlines_tab, name)

    def clear_form():
        """Clear every box in the airline form."""
        if not ok_to_leave_form():
            return
        for entry in airline_entries.values():
            entry.config(state="normal")
            entry.delete(0, "end")
        airline_entries["ID"].config(state="readonly")
        update_button.config(state="disabled")
        delete_button.config(state="disabled")
        show_message(message_label, "Form cleared. Fill in the details "
                                    "to add a new airline.")
        airline_list.selection_remove(airline_list.selection())
        remember_form()

    def fill_form(event):
        """Show the details of the chosen airline in the form."""
        selected = airline_list.selection()
        if not selected:
            return
        # The airline already in the form: nothing to change
        if selected[0] == airline_entries["ID"].get():
            return
        if not ok_to_leave_form():
            reselect_row(airline_list, airline_entries["ID"].get())
            return
        airline_id = int(selected[0])
        for airline in records_of_type(records, "airline"):
            if airline["ID"] == airline_id:
                for field, entry in airline_entries.items():
                    entry.config(state="normal")
                    entry.delete(0, "end")
                    entry.insert(0, airline[field])
                airline_entries["ID"].config(state="readonly")
                update_button.config(state="normal")
                delete_button.config(state="normal")
                company_name = airline["Company Name"]
                show_message(message_label, "Showing " + company_name +
                             ". Update details and click Update.")
                remember_form()

    airline_list.bind("<<TreeviewSelect>>", fill_form)

    def check_form():
        """Check the form and point to the first problem, if any."""
        values = read_entries(airline_entries)
        missing = first_missing_field(values, AIRLINE_REQUIRED)
        if missing:
            show_message(message_label, missing + " is required.", "error")
            airline_entries[missing].focus_set()
            return False
        return True

    def create_airline():
        """Check the form, then add it as a new airline."""
        if check_form():
            # To connect: create_record(records, new_airline) from records.py
            show_message(message_label, "The details are valid. Saving will "
                         "work once the record functions are connected.",
                         "success")

    def update_airline():
        """Check the form, then save the changes to the chosen airline."""
        if check_form():
            # To connect: update_record(records, "airline", ID, new_values)
            show_message(message_label, "The details are valid. Saving will "
                         "work once the record functions are connected.",
                         "success")

    def delete_airline():
        """Ask first, then delete the chosen airline."""
        selected = airline_list.selection()
        if not selected:
            return
        values = airline_list.item(selected[0], "values")
        name = values[1]
        if confirm_delete(airlines_tab, name):
            # To connect: delete_record(records, "airline", ID) from records.py
            show_message(message_label, "Delete confirmed. Deleting will "
                         "work once the record functions are connected.",
                         "success")
        else:
            show_message(message_label, name + " was not deleted.")

    # Buttons in the same places as on the Clients tab
    button_bar = ttk.Frame(airlines_tab)
    button_bar.pack(fill="x", padx=10)

    create_button = ttk.Button(button_bar, text="Create",
                               command=create_airline)
    create_button.pack(side="left", padx=5)
    update_button = ttk.Button(button_bar, text="Update",
                               command=update_airline)
    update_button.pack(side="left", padx=5)
    clear_button = ttk.Button(button_bar, text="Clear", command=clear_form)
    clear_button.pack(side="left", padx=5)
    delete_button = ttk.Button(button_bar, text="Delete",
                               command=delete_airline)
    delete_button.pack(side="right", padx=5)

    # Update and Delete stay greyed out until a record is selected
    update_button.config(state="disabled")
    delete_button.config(state="disabled")

    # Message line shows the agent what happened or what to do
    message_label = ttk.Label(
        airlines_tab,
        text="Select an airline from the list, "
             "or fill in the form to add one.")
    message_label.pack(anchor="w", padx=10, pady=10)

    # Search: the Search button, Enter and every key typed filter the list
    def run_search(event=None):
        """Show only the airlines with the search text in any column."""
        text = search_field.get().strip()
        for row in airline_list.get_children():
            airline_list.delete(row)
        show_airlines(airline_list, records_of_type(records, "airline"))
        keep_matching_rows(airline_list, text)
        update_count()
        reselect_row(airline_list, airline_entries["ID"].get())
        show_search_result(message_label, airline_list, "airlines", text)

    search_button.config(command=run_search)
    search_field.bind("<KeyRelease>", run_search)

    # Show all and the Esc key empty the search box and show every airline
    def show_all(event=None):
        """Empty the search box and show every airline again."""
        search_field.delete(0, "end")
        run_search()

    show_all_button.config(command=show_all)
    search_field.bind("<Escape>", show_all)

    # Remember the starting form, so changes can be spotted
    remember_form()

    # Give back the check, so the window can use it when closing
    return ok_to_leave_form


def create_flights_tab(flights_tab, records):
    """Create the Flights tab: search bar, list, form, buttons, message."""

    # Search bar with Search and Show all buttons, same as on the other tabs
    search_bar = ttk.Frame(flights_tab)
    search_bar.pack(fill="x", padx=10, pady=10)

    search_title = ttk.Label(search_bar, text="Search flights:")
    search_title.pack(side="left")

    search_field = ttk.Entry(search_bar, width=40)
    search_field.pack(side="left", padx=5)

    search_button = ttk.Button(search_bar, text="Search")
    search_button.pack(side="left")

    show_all_button = ttk.Button(search_bar, text="Show all")
    show_all_button.pack(side="left", padx=5)

    # Flight list with names instead of ID numbers, soonest flight first
    list_frame = ttk.Frame(flights_tab)
    list_frame.pack(fill="both", expand=True, padx=10)

    columns = ("id", "date", "client", "airline", "from", "to")
    flight_list = ttk.Treeview(list_frame, columns=columns,
                               show="headings", height=10)

    flight_list.heading("id", text="ID")
    flight_list.heading("date", text="Date & Time")
    flight_list.heading("client", text="Client")
    flight_list.heading("airline", text="Airline")
    flight_list.heading("from", text="From")
    flight_list.heading("to", text="To")

    flight_list.column("id", width=55, stretch=False)
    flight_list.column("date", width=120)
    flight_list.column("client", width=190)
    flight_list.column("airline", width=160)
    flight_list.column("from", width=120)
    flight_list.column("to", width=120)

    # Scrollbar, so every flight can be reached
    list_scrollbar = ttk.Scrollbar(list_frame, orient="vertical",
                                   command=flight_list.yview)
    list_scrollbar.pack(side="right", fill="y")
    flight_list.configure(yscrollcommand=list_scrollbar.set)

    flight_list.pack(side="left", fill="both", expand=True)
    show_flights(flight_list, records_of_type(records, "flight"),
                 records_of_type(records, "client"),
                 records_of_type(records, "airline"))

    # Count under the list, so the agent knows how many flights are shown
    count_label = ttk.Label(flights_tab)
    count_label.pack(anchor="w", padx=10)

    def update_count():
        """Show how many flights are in the list right now."""
        shown = len(flight_list.get_children())
        total = len(records_of_type(records, "flight"))
        count_label.config(text="Showing " + str(shown) + " of " +
                                str(total) + " flights")

    update_count()

    # Flight Details form from my sketch, in the order of a booking call:
    # who, where, when, and then which airline
    flight_form = ttk.LabelFrame(flights_tab, text="Flight Details")
    flight_form.pack(fill="x", padx=10, pady=10)

    # The ID is shown automatically, so the agent cannot type it
    id_label = ttk.Label(flight_form, text="ID (automatic)")
    id_label.grid(row=0, column=0, padx=5, pady=3, sticky="w")
    id_entry = ttk.Entry(flight_form, width=34, state="readonly")
    id_entry.grid(row=0, column=1, padx=5, pady=3, sticky="w")

    # Who: a drop-down list, so the agent can only pick a real client
    client_label = ttk.Label(flight_form, text="Client*")
    client_label.grid(row=1, column=0, padx=5, pady=3, sticky="w")
    client_choices = make_choices(records_of_type(records, "client"))
    client_box = ttk.Combobox(flight_form, width=32, state="readonly",
                              values=client_choices)
    client_box.grid(row=1, column=1, padx=5, pady=3, sticky="w")

    # Where: city boxes suggest every city already used, but a new one can
    # be typed. The swap button sits between them, as on flight websites.
    cities = city_choices(records_of_type(records, "client"),
                          records_of_type(records, "flight"))

    def swap_cities():
        """Swap From and To, which is handy for a return flight."""
        start_city = from_box.get()
        end_city = to_box.get()
        from_box.set(end_city)
        to_box.set(start_city)
        # Show the new route, or a short message if only one city is filled
        if start_city and end_city:
            show_message(message_label, "Route swapped: " + end_city +
                         " → " + start_city + ".", "success")
        else:
            show_message(message_label, "From and To swapped.", "success")

    from_label = ttk.Label(flight_form, text="From*")
    from_label.grid(row=2, column=0, padx=5, pady=3, sticky="w")
    from_area = ttk.Frame(flight_form)
    from_area.grid(row=2, column=1, padx=5, pady=3, sticky="w")
    from_box = ttk.Combobox(from_area, width=26, values=cities)
    from_box.pack(side="left")
    swap_button = ttk.Button(from_area, text="⇄", width=3,
                             command=swap_cities)
    swap_button.pack(side="left", padx=(5, 0))

    to_label = ttk.Label(flight_form, text="To*")
    to_label.grid(row=2, column=2, padx=5, pady=3, sticky="w")
    to_box = ttk.Combobox(flight_form, width=26, values=cities)
    to_box.grid(row=2, column=3, padx=5, pady=3, sticky="w")

    # Smart default: choosing a client fills From with the client's city,
    # but only if From is still empty, so the agent's typing is never lost
    def client_chosen(event):
        """Fill From with the chosen client's city, if From is empty."""
        if from_box.get():
            name = choice_name(client_box.get())
            show_message(message_label, "Client set to " + name + ".")
            return
        client_id = int(client_box.get().split(" – ")[0])
        for client in records_of_type(records, "client"):
            if client["ID"] == client_id and client["City"]:
                from_box.set(client["City"])
                show_message(message_label, "From set to " + client["City"] +
                             ", the client's city. Change it if needed.")

    client_box.bind("<<ComboboxSelected>>", client_chosen)

    # When: arrow boxes for the date in the same order as the list (year,
    # month, day), so the agent cannot type an impossible date like month 13
    today = date.today()

    date_label = ttk.Label(flight_form, text="Date*")
    date_label.grid(row=3, column=0, padx=5, pady=3, sticky="w")
    date_boxes = ttk.Frame(flight_form)
    date_boxes.grid(row=3, column=1, padx=5, pady=3, sticky="w")

    year_box = ttk.Spinbox(date_boxes, from_=today.year, to=today.year + 4,
                           width=5, state="readonly")
    year_box.pack(side="left")
    year_dash = ttk.Label(date_boxes, text="-")
    year_dash.pack(side="left")
    month_box = ttk.Spinbox(date_boxes, from_=1, to=12, width=3,
                            format="%02.0f", wrap=True, state="readonly")
    month_box.pack(side="left")
    month_dash = ttk.Label(date_boxes, text="-")
    month_dash.pack(side="left")
    day_box = ttk.Spinbox(date_boxes, from_=1, to=31, width=3,
                          format="%02.0f", wrap=True, state="readonly")
    day_box.pack(side="left")

    # Arrow boxes for the time on the 24-hour clock, minutes in steps of 5
    time_label = ttk.Label(flight_form, text="Time*")
    time_label.grid(row=3, column=2, padx=5, pady=3, sticky="w")
    time_boxes = ttk.Frame(flight_form)
    time_boxes.grid(row=3, column=3, padx=5, pady=3, sticky="w")

    hour_box = ttk.Spinbox(time_boxes, from_=0, to=23, width=3,
                           format="%02.0f", wrap=True, state="readonly")
    hour_box.pack(side="left")
    time_colon = ttk.Label(time_boxes, text=":")
    time_colon.pack(side="left")
    minute_box = ttk.Spinbox(time_boxes, from_=0, to=55, increment=5,
                             width=3, format="%02.0f", wrap=True,
                             state="readonly")
    minute_box.pack(side="left")
    time_hint = ttk.Label(time_boxes, text="(24-hour)")
    time_hint.pack(side="left", padx=5)

    def show_date_and_time(date_text):
        """Put a "YYYY-MM-DD HH:MM" date and time into the arrow boxes."""
        year_box.set(date_text[0:4])
        month_box.set(date_text[5:7])
        day_box.set(date_text[8:10])
        hour_box.set(date_text[11:13])
        minute_box.set(date_text[14:16])

    # Start with today's date at 12:00, so the agent only changes what differs
    start_date = today.strftime("%Y-%m-%d") + " 12:00"
    show_date_and_time(start_date)

    # Which airline: last, because it is chosen once the route and time are
    # known. A drop-down list, so the agent can only pick a real airline.
    airline_label = ttk.Label(flight_form, text="Airline*")
    airline_label.grid(row=4, column=0, padx=5, pady=3, sticky="w")
    airline_choices = make_choices(records_of_type(records, "airline"))
    airline_box = ttk.Combobox(flight_form, width=32, state="readonly",
                               values=airline_choices)
    airline_box.grid(row=4, column=1, padx=5, pady=3, sticky="w")

    # Note that explains the stars on the labels
    required_note = ttk.Label(flight_form,
                              text="Fields marked * are required.")
    required_note.grid(row=5, column=0, columnspan=4, padx=5, pady=3,
                       sticky="w")

    def refresh_lists():
        """Rebuild the flight list and drop-downs from the shared records."""
        clients = records_of_type(records, "client")
        airlines = records_of_type(records, "airline")
        flights = records_of_type(records, "flight")

        # Flight list and count, so changed names and new flights show,
        # keeping only the flights that match the search text
        for row in flight_list.get_children():
            flight_list.delete(row)
        show_flights(flight_list, flights, clients, airlines)
        keep_matching_rows(flight_list, search_field.get().strip())
        update_count()
        reselect_row(flight_list, id_entry.get())

        # Drop-down lists, so new or renamed clients and airlines show
        client_choices.clear()
        client_choices.extend(make_choices(clients))
        client_box.config(values=client_choices)
        airline_choices.clear()
        airline_choices.extend(make_choices(airlines))
        airline_box.config(values=airline_choices)

        # City suggestions, so new cities are suggested too
        new_cities = city_choices(clients, flights)
        from_box.config(values=new_cities)
        to_box.config(values=new_cities)

    def tab_opened(event):
        """Refresh the Flights tab every time it is shown."""
        refresh_lists()

    flights_tab.bind("<Map>", tab_opened)

    def read_form():
        """Read the flight form, with the date and time as one value."""
        values = read_entries(flight_boxes)
        values["Date"] = (year_box.get() + "-" + month_box.get() + "-" +
                          day_box.get() + " " + hour_box.get() + ":" +
                          minute_box.get())
        return values

    # The form as it was last filled or cleared, to spot unsaved changes
    saved_form = {}

    def remember_form():
        """Remember the form as it is now, to compare with it later."""
        saved_form.clear()
        saved_form.update(read_form())

    def ok_to_leave_form():
        """Give True if nothing is unsaved, or the agent discards it."""
        if read_form() == saved_form:
            return True
        if id_entry.get():
            name = "flight " + id_entry.get()
        else:
            name = "the new flight"
        return confirm_discard(flights_tab, name)

    def clear_form():
        """Empty the flight form, ready to add a new flight."""
        if not ok_to_leave_form():
            return
        id_entry.config(state="normal")
        id_entry.delete(0, "end")
        id_entry.config(state="readonly")
        client_box.set("")
        from_box.set("")
        to_box.set("")
        show_date_and_time(start_date)
        airline_box.set("")
        update_button.config(state="disabled")
        delete_button.config(state="disabled")
        show_message(message_label, "Form cleared. Fill in the details "
                                    "to add a new flight.")
        flight_list.selection_remove(flight_list.selection())
        remember_form()

    def fill_form(event):
        """Show the details of the chosen flight in the form."""
        selected = flight_list.selection()
        if not selected:
            return
        # The flight already in the form: nothing to change
        if selected[0] == id_entry.get():
            return
        if not ok_to_leave_form():
            reselect_row(flight_list, id_entry.get())
            return
        flight_id = int(selected[0])
        for flight in records_of_type(records, "flight"):
            if flight["ID"] == flight_id:
                id_entry.config(state="normal")
                id_entry.delete(0, "end")
                id_entry.insert(0, flight["ID"])
                id_entry.config(state="readonly")
                client_text = find_choice(client_choices, flight["Client_ID"])
                client_box.set(client_text)
                from_box.set(flight["Start City"])
                to_box.set(flight["End City"])
                show_date_and_time(flight["Date"])
                airline_box.set(find_choice(airline_choices,
                                            flight["Airline_ID"]))
                update_button.config(state="normal")
                delete_button.config(state="normal")
                show_message(
                    message_label,
                    "Showing flight " + str(flight_id) + ": " +
                    choice_name(client_text) + ", " +
                    flight["Start City"] + " → " + flight["End City"] +
                    ". Update details and click Update.")
                remember_form()

    flight_list.bind("<<TreeviewSelect>>", fill_form)

    # The boxes that must be filled in, by the names used in messages
    flight_boxes = {"Client": client_box, "From": from_box, "To": to_box,
                    "Airline": airline_box}

    def past_date_confirmed(flight_time):
        """Ask before saving a flight in the past, as it may be a mistake."""
        when = (date_in_words(flight_time.year, flight_time.month,
                              flight_time.day) +
                " at " + flight_time.strftime("%H:%M"))
        answer = messagebox.askyesno(
            "Flight in the past",
            "This flight is on " + when + ", which is in the past. " +
            "Save it anyway?",
            icon="warning", default="no", parent=flights_tab)
        if not answer:
            show_message(message_label, "Not saved. Change the date or "
                         "time and try again.", "warning")
            day_box.focus_set()
        return answer

    def check_form():
        """Check the form and point to the first problem, if any."""
        values = read_entries(flight_boxes)
        missing = first_missing_field(values, FLIGHT_REQUIRED)
        if missing:
            show_message(message_label, missing + " is required.", "error")
            flight_boxes[missing].focus_set()
            return False
        if values["From"].lower() == values["To"].lower():
            show_message(message_label, "From and To must be different "
                         "cities.", "error")
            to_box.focus_set()
            return False
        year = int(year_box.get())
        month = int(month_box.get())
        day = int(day_box.get())
        flight_time = real_date(year, month, day, int(hour_box.get()),
                                int(minute_box.get()))
        if flight_time is None:
            show_message(message_label, date_in_words(year, month, day) +
                         " is not a real date.", "error")
            day_box.focus_set()
            return False
        if flight_time < datetime.now():
            return past_date_confirmed(flight_time)
        return True

    def create_flight():
        """Check the form, then add it as a new flight."""
        if check_form():
            # To connect: create_record(records, new_flight) from records.py
            show_message(message_label, "The details are valid. Saving will "
                         "work once the record functions are connected.",
                         "success")

    def update_flight():
        """Check the form, then save the changes to the chosen flight."""
        if check_form():
            # To connect: update_record(records, "flight", ID, new_values)
            show_message(message_label, "The details are valid. Saving will "
                         "work once the record functions are connected.",
                         "success")

    def delete_flight():
        """Ask first, then delete the chosen flight."""
        selected = flight_list.selection()
        if not selected:
            return
        values = flight_list.item(selected[0], "values")
        name = ("flight " + str(values[0]) + " (" + values[2] + ", " +
                values[4] + " → " + values[5] + ")")
        if confirm_delete(flights_tab, name):
            # To connect: delete_record(records, "flight", ID) from records.py
            show_message(message_label, "Delete confirmed. Deleting will "
                         "work once the record functions are connected.",
                         "success")
        else:
            show_message(message_label, name + " was not deleted.")

    # Buttons in the same places as on the other tabs
    button_bar = ttk.Frame(flights_tab)
    button_bar.pack(fill="x", padx=10)

    create_button = ttk.Button(button_bar, text="Create",
                               command=create_flight)
    create_button.pack(side="left", padx=5)
    update_button = ttk.Button(button_bar, text="Update",
                               command=update_flight)
    update_button.pack(side="left", padx=5)
    clear_button = ttk.Button(button_bar, text="Clear", command=clear_form)
    clear_button.pack(side="left", padx=5)
    delete_button = ttk.Button(button_bar, text="Delete",
                               command=delete_flight)
    delete_button.pack(side="right", padx=5)

    # Update and Delete stay greyed out until a record is selected
    update_button.config(state="disabled")
    delete_button.config(state="disabled")

    # Message line shows the agent what happened or what to do
    message_label = ttk.Label(
        flights_tab,
        text="Select a flight from the list, or fill in the form to add one.")
    message_label.pack(anchor="w", padx=10, pady=10)

    # Search: the Search button, Enter and every key typed filter the list
    def run_search(event=None):
        """Show only the flights with the search text in any column."""
        refresh_lists()
        show_search_result(message_label, flight_list, "flights",
                           search_field.get().strip())

    search_button.config(command=run_search)
    search_field.bind("<KeyRelease>", run_search)

    # Show all and the Esc key empty the search box and show every flight
    def show_all(event=None):
        """Empty the search box and show every flight again."""
        search_field.delete(0, "end")
        run_search()

    show_all_button.config(command=show_all)
    search_field.bind("<Escape>", show_all)

    # Remember the starting form, so changes can be spotted
    remember_form()

    # Give back the check, so the window can use it when closing
    return ok_to_leave_form


def create_main_window():
    """Open the main window with one tab for every type of record."""

    main_window = tk.Tk()
    main_window.title("Travel Agent Record Manager")
    main_window.geometry("1000x650")

    # Form titles: the app's normal font, but bold
    title_font = font.nametofont("TkDefaultFont").copy()
    title_font.configure(weight="bold")
    style = ttk.Style()
    style.configure("TLabelframe.Label", font=title_font)

    # All records in one list of dictionaries, as the brief asks.
    # For now the sample data; later: records = load_records(DATA_FILE)
    records = SAMPLE_CLIENTS + SAMPLE_AIRLINES + SAMPLE_FLIGHTS

    # Make the tabs bigger when the window is resized
    tab_bar = ttk.Notebook(main_window)
    tab_bar.pack(fill="both", expand=True)

    # One tab for each type of record in the same order as in my sketch
    clients_tab = ttk.Frame(tab_bar)
    tab_bar.add(clients_tab, text="Clients")
    clients_form_check = create_clients_tab(clients_tab, records)

    airlines_tab = ttk.Frame(tab_bar)
    tab_bar.add(airlines_tab, text="Airlines")
    airlines_form_check = create_airlines_tab(airlines_tab, records)

    flights_tab = ttk.Frame(tab_bar)
    tab_bar.add(flights_tab, text="Flights")
    flights_form_check = create_flights_tab(flights_tab, records)

    def close_app():
        """Check every form for unsaved changes, then close the window."""
        for ok_to_leave_form in (clients_form_check, airlines_form_check,
                                 flights_form_check):
            if not ok_to_leave_form():
                return
        # To connect: save_records(records, DATA_FILE) from storage.py
        main_window.destroy()

    # Run close_app when the agent closes the window
    main_window.protocol("WM_DELETE_WINDOW", close_app)

    return main_window


if __name__ == "__main__":
    main_window = create_main_window()
    main_window.mainloop()
