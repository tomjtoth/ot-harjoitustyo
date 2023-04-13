from tkinter import messagebox, Tk, Listbox, Button, Label, W, Canvas
from ui.common import View
from backend.backend import backend


class DrawingView(View):
    """drawing view"""

    def __init__(self, master, menu_view, dwg):
        """creates the main drawing view"""

        super().__init__(master, None, menu_view)
        self._curr_user = backend.get_curr_user()
        self._curr_dwg = dwg
        self._create_widgets()

    def _create_widgets(self):
        Label(self._frame,
                text=f"Login: {self._curr_user.name}"
            ).grid(row=0, column=0, columnspan=2)

        Button(self._frame, text='Menu', command=self._handle_prev).grid(columnspan=2)
        Button(self._frame, text='▯ rect').grid(column=0, row=2)
        Button(self._frame, text='O circ').grid(column=1, row=2)
        Button(self._frame, text='W poly').grid(column=0, row=3)
        Button(self._frame, text='/ line').grid(column=1, row=3)

        Label(self._frame, text='colors').grid(columnspan=2, row=4)
        Button(self._frame, bg='black').grid(column=0, row=5)
        Button(self._frame, bg='black').grid(column=1, row=5)
        Button(self._frame, bg='white').grid(column=0, row=6)
        Button(self._frame, bg='white').grid(column=1, row=6)
        Button(self._frame, bg='red').grid(column=0, row=7)
        Button(self._frame, bg='red').grid(column=1, row=7)
        Button(self._frame, bg='green').grid(column=0, row=8)
        Button(self._frame, bg='green').grid(column=1, row=8)
        Button(self._frame, bg='blue').grid(column=0, row=9)
        Button(self._frame, bg='blue').grid(column=1, row=9)
        Button(self._frame, text='custom').grid(column=0, row=10)
        Button(self._frame, text='custom').grid(column=1, row=10)

        Label(self._frame, text='etc.').grid(columnspan=2, row=11)
        # adding text (?)
        Button(self._frame, text='Aa').grid(column=0, row=12)
        Button(self._frame, text='placeholder').grid(column=1, row=12)

        canv = Canvas(self._frame, width=800, height=600, bg='white').grid(column=2, row=0, rowspan=13)
        
        

        # add extra controls/functionalities
        if self._curr_user.teacher:
            pass
