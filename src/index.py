#!/usr/bin/env python3

from tkinter import Tk
from ui.ui import Ui

def main():
    window = Tk()
    window.title('SVG artistic program')

    ui = Ui(window)
    ui.show_login()

    window.mainloop()


if __name__ == '__main__':
    main()
