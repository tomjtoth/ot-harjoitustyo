#!/usr/bin/env python3

from tkinter import Tk
from database.backend import Backend
from ui.ui import Ui

def main():
    backend = Backend()
    window = Tk()
    window.title('SVG artistic program')

    ui_view = Ui(window)

    window.mainloop()


if __name__ == '__main__':
    main()