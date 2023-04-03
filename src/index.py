#!/usr/bin/env python3
import tkinter as tk

# Messagebox is not visible via above tk.messagebox...
from tkinter import messagebox as msg

# this will be backed by a table in sqlite
users = {'test':'test'}


class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        tk.Label(self, text='username:').grid(row = 0, column = 0, sticky = tk.W, pady = 2)
        self.username = tk.Entry(self)
        self.username.grid(row = 0, column = 1, pady = 2)
        
        tk.Label(self, text='password:').grid(row = 1, column = 0, sticky = tk.W, pady = 2)
        self.password = tk.Entry(self, show="*")
        self.password.grid(row = 1, column = 1, pady = 2)


        tk.Button(self, text='Login/register', command=self.processInput).grid()
        tk.Button(self, text='Quit', command=self.quit).grid()
    
    def processInput(self):
        user = self.username.get()
        pw = self.password.get()
        if user not in users:
            users[user] = pw
            msg.showinfo("Registration", "user successfully created")
        elif users[user] != pw:
            msg.showerror("Login failed", "wrong password")
        else:
            msg.showinfo("Login succeeded", "you're in!")
            pass
        


app = Application()
app.master.title('SVG artistic program')
app.mainloop()