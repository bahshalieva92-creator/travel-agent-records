"""This is the main window of the Travel Agent Record Manager app."""

import tkinter as tk
from tkinter import ttk
from tkinter import font

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


def create_clients_tab(clients_tab):
    """Create search bar and the clients list on the Clients tab."""

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
    show_clients(client_list, SAMPLE_CLIENTS)

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

    def clear_form():
        """Clear every box in the form."""
        for entry in client_entries.values():
            entry.config(state="normal")
            entry.delete(0, "end")
        client_entries["ID"].config(state="readonly")
        message_label.config(text="Form cleared. Fill in the details "
                                  "to add a new client.")
        client_list.selection_remove(client_list.selection())
        
    def fill_form(event):
        """Show the details of the chosen client in the form."""
        selected = client_list.selection()
        if not selected:
            return
        client_id = int(selected[0])
        for client in SAMPLE_CLIENTS:
            if client["ID"] == client_id:
                for field, entry in client_entries.items():
                    entry.config(state="normal")
                    entry.delete(0, "end")
                    entry.insert(0, client[field])
                client_entries["ID"].config(state="readonly")
                message_label.config(text="Showing " + client["Name"] +
                                     ". Update details and click Update.")

    client_list.bind("<<TreeviewSelect>>", fill_form)

    # Buttons from my sketch: Delete set apart on the right
    button_bar = ttk.Frame(clients_tab)
    button_bar.pack(fill="x", padx=10)

    create_button = ttk.Button(button_bar, text="Create")
    create_button.pack(side="left", padx=5)
    update_button = ttk.Button(button_bar, text="Update")
    update_button.pack(side="left", padx=5)
    clear_button = ttk.Button(button_bar, text="Clear", command=clear_form)
    clear_button.pack(side="left", padx=5)
    delete_button = ttk.Button(button_bar, text="Delete")
    delete_button.pack(side="right", padx=5)

    # Message line shows the agent what happened or what to do
    message_label = ttk.Label(
        clients_tab,
        text="Select a client from the list, or fill in the form to add one.")
    message_label.pack(anchor="w", padx=10, pady=10)
    

def create_airlines_tab(airlines_tab):
    """Create the search bar and the airline list on the Airlines tab."""

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
    show_airlines(airline_list, SAMPLE_AIRLINES)


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

    # Make the tabs bigger when the window is resized
    tab_bar = ttk.Notebook(main_window)
    tab_bar.pack(fill="both", expand=True)

    # One tab for each type of record in the same order as in my sketch
    clients_tab = ttk.Frame(tab_bar)
    tab_bar.add(clients_tab, text="Clients")
    create_clients_tab(clients_tab)

    airlines_tab = ttk.Frame(tab_bar)
    tab_bar.add(airlines_tab, text="Airlines")
    create_airlines_tab(airlines_tab)

    flights_tab = ttk.Frame(tab_bar)
    tab_bar.add(flights_tab, text="Flights")

    return main_window


if __name__ == "__main__":
    main_window = create_main_window()
    main_window.mainloop()
