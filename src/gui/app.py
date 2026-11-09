# This is the main window of the Travel Agent Record Manager app

import tkinter as tk
from tkinter import ttk
 

def create_main_window():
    """Open the main window with one tab for every type of record."""

    main_window = tk.Tk()
    main_window.title("Travel Agent Record Manager")
    main_window.geometry("1000x650")

    # Make the tabs bigger when the window is resized
    tab_bar = ttk.Notebook(main_window)
    tab_bar.pack(fill="both", expand=True)

    
    # One tab per every type of record in the same order as in my sketch
    clients_tab = ttk.Frame(tab_bar)
    tab_bar.add(clients_tab, text="Clients")

    airlines_tab = ttk.Frame(tab_bar)
    tab_bar.add(airlines_tab, text="Airlines")

    flights_tab = ttk.Frame(tab_bar)
    tab_bar.add(flights_tab, text="Flights")

    return main_window


if __name__ == "__main__":
    main_window = create_main_window()
    main_window.mainloop()
