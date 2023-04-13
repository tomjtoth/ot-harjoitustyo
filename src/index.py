#!/usr/bin/env python3

from tkinter import Tk
from ui.ui import Ui

def main():
    tk_window = Tk()
    tk_window.title('SVG artistic program')

    ui_window = Ui(tk_window)
    ui_window.show_login()

    tk_window.mainloop()


if __name__ == '__main__':
    main()
