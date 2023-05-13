from tkinter import Button, Label, Canvas, Radiobutton, IntVar, DISABLED, NORMAL
from ui.common import View, TITLE
from ui.prompt_text import PromptText
from backend.dwg_mgmt import dwg_mgr, RECTANGLE, OVAL, LINE, TEXT


class DrawingView(View):
    """3rd main view, used for adding features to the dwg
    """

    def __init__(self, master, menu_view: callable):
        """Creates the main dwg view
        """
        super().__init__(master, None, menu_view)
        self._curr_dwg = dwg_mgr.get_curr_dwg()
        self._rows = 5
        self._create_widgets()

    def _add_clr_btn(self, color: str):
        """Adds colored buttons for border and filling separately

        Args:
            color (str): could be anything tkinter knows
        """
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
        """Populates the widgets in the view
        """
        Button(self._frame, text="Save and Exit",
               command=self._save_and_exit
               ).grid(columnspan=2)

        self._undo_btn = Button(self._frame, text="undo",
                                command=self._undo)
        self._undo_btn.grid(column=0, row=1)

        self._redo_btn = Button(self._frame, text="redo", state=DISABLED,
                                command=self._redo)
        self._redo_btn.grid(column=1, row=1)

        self._rb_val = IntVar(self._frame, value=RECTANGLE)

        Radiobutton(self._frame, text="rect",
                    value=RECTANGLE, variable=self._rb_val,
                    command=lambda: dwg_mgr.set_cmd(RECTANGLE)
                    ).grid(column=0, row=2)

        Radiobutton(self._frame, text="oval",
                    value=OVAL, variable=self._rb_val,
                    command=lambda: dwg_mgr.set_cmd(OVAL)
                    ).grid(column=1, row=2)

        Radiobutton(self._frame, text="text",
                    value=TEXT, variable=self._rb_val,
                    command=lambda: dwg_mgr.set_cmd(TEXT)
                    ).grid(column=0, row=3)

        Radiobutton(self._frame, text="line",
                    value=LINE, variable=self._rb_val,
                    command=lambda: dwg_mgr.set_cmd(LINE)
                    ).grid(column=1, row=3)

        Label(self._frame, text="↓ border - fill ↓").grid(columnspan=2, row=4)
        for color in "black white red green blue yellow purple gray brown pink orange lime".split():
            self._add_clr_btn(color)

        canv = Canvas(
            self._frame,
            width=self._curr_dwg.width,
            height=self._curr_dwg.height,
            bg="white"
        )
        canv.grid(column=2, row=0, rowspan=20)
        dwg_mgr.set_cmd(RECTANGLE)
        dwg_mgr.set_border("red")
        dwg_mgr.set_fill("green")

        self._master.title(f"{TITLE} {self._curr_dwg.name}")
        dwg_mgr.set_canvas(canv, self.btn_state_setter)
        canv.bind("<Button-1>", dwg_mgr.b1_dn)
        canv.bind("<B1-Motion>", dwg_mgr.b1_mv)
        canv.bind("<B1-ButtonRelease>", dwg_mgr.b1_up)

        dwg_mgr.set_text_prompter(self.prompt_text)

    def _save_and_exit(self):
        """Saves the current drawing to database and changes view
        """
        self._master.title(TITLE)
        dwg_mgr.save_curr_dwg()
        self._handle_prev()

    def prompt_text(self):
        """Prompts the user for input

        Returns:
            str: the user input
        """
        return PromptText(self._frame,
                          "Text to add",
                          {"text": "text:"},
                          {},
                          {"text": "Add text"}).get()

    def _undo(self):
        """Moves the last feature from dwg to undo stack, also sets button states
        """
        if dwg_mgr.undo():
            self._redo_btn["state"] = NORMAL
        else:
            self._undo_btn["state"] = DISABLED

    def _redo(self):
        """Moves the last feature from the undo stack to the dwg, also sets button states
        """
        if dwg_mgr.redo():
            self._undo_btn["state"] = NORMAL
        else:
            self._redo_btn["state"] = DISABLED

    def btn_state_setter(self):
        """dwg_mgr calls this to set the button state upon adding features
        """
        self._undo_btn["state"] = NORMAL
        self._redo_btn["state"] = DISABLED
