from tkinter import Toplevel, StringVar, IntVar, Label, Entry, Button
from backend.backend import backend
from entities.drawing import Drawing

class PromptNewDrawing(Toplevel):
    """Queries data about the new drawing and assigns it to backend"""

    def __init__(self, master):
        """constructor, lol (?)"""

        super().__init__(master)
        self.title('New DWG')
        self.resizable(False, False)

        name = StringVar(self, value='jotain uusi')
        Label(self, text='name:').grid(column=0, row=0)
        Entry(self, textvariable=name).grid(column=1, row=0)

        width = IntVar(self, value=800)
        Label(self, text='width:').grid(column=0, row=1)
        Entry(self, textvariable=width).grid(column=1, row=1)

        height = IntVar(self, value=600)
        Label(self, text='height:').grid(column=0, row=2)
        Entry(self, textvariable=height).grid(column=1, row=2)

        Button(self, text='Create', command=lambda: self._new_dwg(name, width, height, self.destroy)
                ).grid(columnspan=2, row=3)

        self.wait_window()
    
    def _new_dwg(self, name, width, height, self_destruct):
        """helper method for setting up a new drawing"""

        backend.set_curr_dwg(Drawing(name.get(), width.get(), height.get()))
        self_destruct()


