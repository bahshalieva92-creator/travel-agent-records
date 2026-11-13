"""Open the main window of the Travel Agent Record Manager."""

from gui.app import create_main_window


if __name__ == "__main__":
    main_window = create_main_window()
    main_window.mainloop()
