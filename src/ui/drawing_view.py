from tkinter import Button, Label, Canvas, Radiobutton, IntVar
from ui.common import View
from backend.backend import backend, RECTANGLE, OVAL, LINE, TEXT

class DrawingView(View):
    """drawing view"""

    def __init__(self, master, menu_view):
        """creates the main drawing view"""

        super().__init__(master, None, menu_view)
        self._curr_user = backend.get_curr_user()
        self._curr_dwg = backend.get_curr_dwg()
        self._rows = 5
        self._create_widgets()

    def _add_clr_btn(self, color: str):
        "adds a button for border and a button for fill"

        Button(self._frame, bg=color,
            command=lambda : backend.set_border(color),
            activebackground=color,
            ).grid(column=0, row=self._rows)

        Button(self._frame,  bg=color,
            command=lambda : backend.set_fill(color),
            activebackground=color,
            ).grid(column=1, row=self._rows)

        self._rows += 1

    # jatkokehari
    def _undo(self):
        pass

    # jatkokehari
    def _redo(self):
        pass

    def _create_widgets(self):

        Button(self._frame, text=f"Logout ({self._curr_user.name})",
            command=self._save_and_exit
            ).grid(columnspan=2)

        self._undo_btn = Button(self._frame, text='undo', state='disabled',
            command=self._undo)
        self._undo_btn.grid(column=0, row=1)

        self._redo_btn = Button(self._frame, text='redo', state='disabled',
            command=self._redo)
        self._redo_btn.grid(column=1, row=1)

        self._rb_val = IntVar(self._frame, value=RECTANGLE)
        
        Radiobutton(self._frame, text='rect',
            value=RECTANGLE, variable=self._rb_val,
            command= lambda : backend.set_cmd(RECTANGLE)
            ).grid(column=0, row=2)

        Radiobutton(self._frame, text='oval',
            value=OVAL, variable=self._rb_val,
            command= lambda : backend.set_cmd(OVAL)
            ).grid(column=1, row=2)

        Radiobutton(self._frame, text='text',
            value=TEXT, variable=self._rb_val,
            command= lambda : backend.set_cmd(TEXT)
            ).grid(column=0, row=3)

        Radiobutton(self._frame, text='line',
            value=LINE, variable=self._rb_val,
            command= lambda : backend.set_cmd(LINE)
            ).grid(column=1, row=3)

        Label(self._frame, text='↓ border - fill ↓').grid(columnspan=2, row=4)
        self._add_clr_btn('black')
        self._add_clr_btn('white')
        self._add_clr_btn('red')
        self._add_clr_btn('green')
        self._add_clr_btn('blue')
        
        # ehkä jatkokehitykseen...
        #Button(self._frame, text='custom').grid(column=0, row=10)
        #Button(self._frame, text='custom').grid(column=1, row=10)

        canv = Canvas(
            self._frame, 
            width=self._curr_dwg.width, 
            height=self._curr_dwg.height, 
            bg='white'
        )
        canv.grid(column=2, row=0, rowspan=20)

        # separating app logic from UI here (?)
        self._master.title(f'Art + {self._curr_dwg.name}')
        backend.set_canvas(canv)
        canv.bind('<Button-1>', backend.b1_dn)
        canv.bind('<B1-Motion>', backend.b1_mv)
        canv.bind('<B1-ButtonRelease>', backend.b1_up)

        backend.set_border('red')
        backend.set_fill('green')
        backend.set_cmd(RECTANGLE)
        
        # add extra controls/functionalities
        if self._curr_user.teacher:
            pass

    def _save_and_exit(self):
        self._master.title('Art +')
        backend.save_curr_dwg()
        self._handle_prev()