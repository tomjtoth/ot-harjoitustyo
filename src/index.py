#!/usr/bin/env python3

from tkinter import Tk, PhotoImage
from ui.ui import Ui

def main():
    tk_window = Tk()
    tk_window.title('Art+')

    tk_window.iconphoto(True, PhotoImage(file='src/ui/van_gogh_icon.png'))

    ui_window = Ui(tk_window)
    ui_window.show_login()

    tk_window.mainloop()


if __name__ == '__main__':
    main()
