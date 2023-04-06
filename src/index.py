#!/usr/bin/env python3

import tkinter as tk
# Messagebox is not visible via above tk.messagebox...
from tkinter import messagebox as msg
from database.database import Backend
import re


class Application(tk.Frame):

    def __init__(self, master=None):
        self.db = Backend()
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.username_re = re.compile(r"^\w{3,}$")

    def create_widgets(self):
        tk.Label(self, text='username:').grid(
            row=0, column=0, sticky=tk.W, pady=2)
        self.username = tk.Entry(self)
        self.username.grid(row=0, column=1, pady=2)

        tk.Label(self, text='password:').grid(
            row=1, column=0, sticky=tk.W, pady=2)
        self.password = tk.Entry(self, show="*")
        self.password.grid(row=1, column=1, pady=2)

        tk.Button(self, text='Login/register',
                  command=self.process_input).grid(columnspan=2)
        tk.Button(self, text='Quit', command=self.quit).grid(columnspan=2)

    def process_input(self):
        username = self.username.get()
        
        if not self.username_re.match(username):
            msg.showerror("invalid username", "usernames should:\n- be more than 3 chars\n- contain only chars from a-zA-Z0-9")
            return
            
        success, teacher = self.db.login_register(
            username, self.password.get())
        if success:
            msg.showinfo(
                "Succeess", f"you're in!{' ... as a teacher' if teacher else ''}")
        else:
            msg.showerror("Login/register failed", "wrong password")


app = Application()
app.master.title('SVG artistic program')
app.mainloop()
