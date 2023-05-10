from tkinter import Button, Label, Canvas, Radiobutton, IntVar, DISABLED, NORMAL
from ui.common import View
from ui.prompt_text import PromptText
from backend.dwg_mgmt import dwg_mgr, RECTANGLE, OVAL, LINE, TEXT


class DrawingView(View):
    """the main drawing view"""

    def __init__(self, master, menu_view: callable):
        """creates the main drawing view"""

        super().__init__(master, None, menu_view)
        self._curr_dwg = dwg_mgr.get_curr_dwg()
        self._rows = 5
        self._create_widgets()

    def _add_clr_btn(self, color: str):
        """adds a button for border and a button for fill"""

        Button(self._frame, bg=color,
               command=lambda: dwg_mgr.set_border(color),
               activebackground=color,
               ).grid(column=0, row=self._rows)

        Button(self._frame,  bg=color,
               command=lambda: dwg_mgr.set_fill(color),
               activebackground=color,
               ).grid(column=1, row=self._rows)

        self._rows += 1

    def _create_widgets(self):
        """creates all the GUI controls"""

        Button(self._frame, text='Save and Exit',
               command=self._save_and_exit
               ).grid(columnspan=2)

        self._undo_btn = Button(self._frame, text='undo',
                                command=self._undo)
        self._undo_btn.grid(column=0, row=1)

        self._redo_btn = Button(self._frame, text='redo', state=DISABLED,
                                command=self._redo)
        self._redo_btn.grid(column=1, row=1)

        self._rb_val = IntVar(self._frame, value=RECTANGLE)

        Radiobutton(self._frame, text='rect',
                    value=RECTANGLE, variable=self._rb_val,
                    command=lambda: dwg_mgr.set_cmd(RECTANGLE)
                    ).grid(column=0, row=2)

        Radiobutton(self._frame, text='oval',
                    value=OVAL, variable=self._rb_val,
                    command=lambda: dwg_mgr.set_cmd(OVAL)
                    ).grid(column=1, row=2)

        Radiobutton(self._frame, text='text',
                    value=TEXT, variable=self._rb_val,
                    command=lambda: dwg_mgr.set_cmd(TEXT)
                    ).grid(column=0, row=3)

        Radiobutton(self._frame, text='line',
                    value=LINE, variable=self._rb_val,
                    command=lambda: dwg_mgr.set_cmd(LINE)
                    ).grid(column=1, row=3)

        Label(self._frame, text='↓ border - fill ↓').grid(columnspan=2, row=4)
        for color in 'black white red green blue yellow purple gray brown pink orange lime'.split():
            self._add_clr_btn(color)

        # ehkä jatkokehitykseen...
        # Button(self._frame, text='custom').grid(column=0, row=10)
        # Button(self._frame, text='custom').grid(column=1, row=10)

        canv = Canvas(
            self._frame,
            width=self._curr_dwg.width,
            height=self._curr_dwg.height,
            bg='white'
        )
        canv.grid(column=2, row=0, rowspan=20)
        dwg_mgr.set_cmd(RECTANGLE)
        dwg_mgr.set_border('red')
        dwg_mgr.set_fill('green')

        # separating app logic from UI here (?)
        self._master.title(f'Art + {self._curr_dwg.name}')
        dwg_mgr.set_canvas(canv, self.undo_btn_enabler)
        canv.bind('<Button-1>', dwg_mgr.b1_dn)
        canv.bind('<B1-Motion>', dwg_mgr.b1_mv)
        canv.bind('<B1-ButtonRelease>', dwg_mgr.b1_up)

        dwg_mgr.set_text_prompter(self.prompt_text)

        # add extra controls/functionalities
        # if self._curr_user.teacher:
        #    pass

    def _save_and_exit(self):
        """Saves the current drawing to database"""

        self._master.title('Art +')
        dwg_mgr.save_curr_dwg()
        self._handle_prev()

    def prompt_text(self):
        """
            makes dwg_mgr able to create a pop-up window
            and prompt the user for text input
        """

        return PromptText(self._frame,
                          'Text to add',
                          {'text': 'text:'},
                          {},
                          {'text': 'Add text'}).get()

    def _undo(self):
        """pushes the last feature from the drawing to the undo stack"""
        if dwg_mgr.undo():
            self._redo_btn['state'] = NORMAL
        else:
            self._undo_btn['state'] = DISABLED

    def _redo(self):
        """pushes 1 feature from undo stack to the drawing"""
        if dwg_mgr.redo():
            self._undo_btn['state'] = NORMAL
        else:
            self._redo_btn['state'] = DISABLED

    def undo_btn_enabler(self):
        """Makes dwg_mgr able to enable the undo button"""
        self._undo_btn['state'] = NORMAL
