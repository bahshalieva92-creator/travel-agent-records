"""This is the main window of the Travel Agent Record Manager app."""

import tkinter as tk
from tkinter import ttk

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


def show_clients(client_list, clients):
    """Show each client as a separate new row in the list."""
    for client in clients:
        client_list.insert("", "end", values=(
            client["ID"], client["Name"], client["Address Line 1"],
            client["Phone Number"], client["City"], client["Country"]))


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
    columns = ("id", "name", "address", "phone", "city", "country")
    client_list = ttk.Treeview(clients_tab, columns=columns,
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
    client_list.pack(fill="both", expand=True, padx=10)
    show_clients(client_list, SAMPLE_CLIENTS)
  

def create_main_window():
    """Open the main window with one tab for every type of record."""

    main_window = tk.Tk()
    main_window.title("Travel Agent Record Manager")
    main_window.geometry("1000x650")

    # Make the tabs bigger when the window is resized
    tab_bar = ttk.Notebook(main_window)
    tab_bar.pack(fill="both", expand=True)

    # One tab for each type of record in the same order as in my sketch
    clients_tab = ttk.Frame(tab_bar)
    tab_bar.add(clients_tab, text="Clients")
    create_clients_tab(clients_tab)

    airlines_tab = ttk.Frame(tab_bar)
    tab_bar.add(airlines_tab, text="Airlines")

    flights_tab = ttk.Frame(tab_bar)
    tab_bar.add(flights_tab, text="Flights")

    return main_window


if __name__ == "__main__":
    main_window = create_main_window()
    main_window.mainloop()
