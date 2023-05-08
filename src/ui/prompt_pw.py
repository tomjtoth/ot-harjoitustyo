from tkinter import Toplevel, StringVar, Label, Entry, Button


class PromptPassword(Toplevel):
    """basic input box for random text inputs"""

    def __init__(self, master, username: str):
        """"""

        super().__init__(master)
        self.title(f'Registering {username}')

        self._password = StringVar(self)
        Label(self, text='repeat password:').grid(column=0, row=0)
        password = Entry(self, textvariable=self._password, show="*")
        password.bind('<Return>', lambda _ev: self.destroy())
        password.grid(column=1, row=0)
        password.focus_set()

        Button(self, text='Confirm user creation', command=self.destroy
               ).grid(columnspan=2, row=3)

    def process(self):
        """method for querying text input"""

        self.wait_window()
        return self._password.get()
