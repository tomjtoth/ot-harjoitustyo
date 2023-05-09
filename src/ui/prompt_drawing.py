from tkinter import Toplevel, StringVar, IntVar, Label, Entry, Button, messagebox


class PromptDrawing(Toplevel):
    """Queries data about the new drawing and assigns it to backend"""

    def __init__(self, master):

        super().__init__(master)
        self.title('New DWG')
        self.resizable(False, False)
        # self.grab_set()

        self._title = StringVar(value='uusi')
        Label(self, text='name:').grid(column=0, row=0)
        entr_t = Entry(self, textvariable=self._title)
        entr_t.grid(column=1, row=0)
        entr_t.bind('<Return>', lambda _ev: entr_w.focus_set())
        entr_t.focus_set()

        self._width = IntVar(self, value=800)
        Label(self, text='width:').grid(column=0, row=1)
        entr_w = Entry(self, textvariable=self._width)
        entr_w.grid(column=1, row=1)
        entr_w.bind('<Return>', lambda _ev: entr_h.focus_set())

        self._height = IntVar(self, value=600)
        Label(self, text='height:').grid(column=0, row=2)
        entr_h = Entry(self, textvariable=self._height)
        entr_h.grid(column=1, row=2)
        entr_h.bind('<Return>', lambda _ev: self._validate())

        Button(self, text='Create', command=self._validate
               ).grid(columnspan=2, row=3)

    def process(self):
        """helper method for setting up a new drawing"""

        self.wait_window()
        return self._title.get(), self._width.get(), self._height.get()

    def _validate(self):
        if self._title.get() == "":
            messagebox.showerror("wrong input", "empty title's are not allowed")
            self.lift()
            return
        try:
            int(self._width.get())
            int(self._height.get())
            self.destroy()
        except:
            messagebox.showerror("wrong input", "width and height should be integer values")
            self.lift()
