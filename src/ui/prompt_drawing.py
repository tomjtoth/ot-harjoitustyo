from tkinter import Toplevel, StringVar, IntVar, Label, Entry, Button


class PromptDrawing(Toplevel):
    """Queries data about the new drawing and assigns it to backend"""

    def __init__(self, master):
        """constructor, lol (?)"""

        super().__init__(master)
        self.title('New DWG')
        self.resizable(False, False)
        # self.grab_set()

        self._title = StringVar(value='uusi')
        Label(self, text='name:').grid(column=0, row=0)
        entr_n = Entry(self, textvariable=self._title)
        entr_n.grid(column=1, row=0)
        entr_n.bind('<Return>', lambda _ev: entr_w.focus_set())
        entr_n.focus_set()

        self._width = IntVar(self, value=800)
        Label(self, text='width:').grid(column=0, row=1)
        entr_w = Entry(self, textvariable=self._width)
        entr_w.grid(column=1, row=1)
        entr_w.bind('<Return>', lambda _ev: entr_h.focus_set())

        self._height = IntVar(self, value=600)
        Label(self, text='height:').grid(column=0, row=2)
        entr_h = Entry(self, textvariable=self._height)
        entr_h.grid(column=1, row=2)
        entr_h.bind('<Return>', lambda _ev: self.destroy())

        Button(self, text='Create', command=self.destroy
               ).grid(columnspan=2, row=3)

    def process(self):
        """helper method for setting up a new drawing"""

        self.wait_window()
        return self._title.get(), self._width.get(), self._height.get()
