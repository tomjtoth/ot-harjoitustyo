#!/usr/bin/env python3

import re
from textwrap import dedent
import tkinter as tk
# Messagebox is not visible via above tk.messagebox...
from tkinter import messagebox as msg
from database.database import Backend


class Application(tk.Frame):

    def __init__(self, master=None):
        self.backend = Backend()
        tk.Frame.__init__(self, master)
        self.grid()
        self._create_widgets()
        self.username_re = re.compile(r"^\w{3,}$")
        self.password_re = re.compile(r"^\w{8,16}$")

    def _create_widgets(self):
        tk.Label(self, text='username:').grid(
            row=0, column=0, sticky=tk.W, pady=2)
        self.username = tk.Entry(self)
        self.username.grid(row=0, column=1, pady=2)

        tk.Label(self, text='password:').grid(
            row=1, column=0, sticky=tk.W, pady=2)
        self.password = tk.Entry(self, show="*")
        self.password.grid(row=1, column=1, pady=2)

        tk.Button(self, text='Login/register',
                  command=self._process_input).grid(columnspan=2)
        tk.Button(self, text='Quit', command=self.quit).grid(columnspan=2)

    def _process_input(self):
        username = self.username.get()
        password = self.password.get()

        if not self.username_re.match(username):
            msg.showerror(
                "invalid username", dedent("""
                usernames should:
                - be more than 3 chars
                - contain only chars from a-zA-Z0-9_
                """))
            return

        if not self.password_re.match(password):
            msg.showerror(
                "invalid password", dedent("""
                passwords should:
                - be between 8 and 16 chars
                - contain only chars from a-zA-Z0-9_
                """))
            return

        success, teacher = self.backend.login_register(
            username, password)
        if success:
            msg.showinfo(
                "Succeess", f"you're in!{' ... as a teacher' if teacher else ''}")

        else:
            msg.showerror("Login/register failed", "wrong password")

    def _show(self):
        pass


if __name__ == "__main__":
    app = Application()
    app.master.title('SVG artistic program')
    app.mainloop()
