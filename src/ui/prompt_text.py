from tkinter import Toplevel, StringVar, Label, Entry, Button
from backend.backend import backend

class PromptNewText(Toplevel):
    """basic input box for random text inputs"""

    def __init__(self, master):
        """"""

        super().__init__()
        self.title('Text to input')

        self._text = StringVar(self, value='jotain')
        Label(self, text='name:').grid(column=0, row=0)
        txt = Entry(self, textvariable=self._text)
        txt.bind('<Return>', self.destroy)
        txt.grid(column=1, row=0)
        txt.focus_set()

        Button(self, text='OK', command=self.destroy
            ).grid(columnspan=2, row=3)

    def process(self):
        """method for querying text input"""
        #backend.set_next_text(self._text.get())
        self.wait_window()
        return self._text.get()
    



