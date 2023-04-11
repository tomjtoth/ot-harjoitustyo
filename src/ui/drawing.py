from tkinter import messagebox, Tk, Listbox, Button, Label, W
from ui.common import View
from backend.backend import backend


class Drawing(View):
    """drawing view"""

    def __init__(self, master, menu_view):
        """creates the main drawing view"""

        super().__init__(master, None, menu_view)
        self._curr_user = backend.get_curr_user()
        self._create_widgets()

    def _create_widgets(self):
        Label(self._frame,
              text=f"You're logged in as {self._curr_user.name}"
              ).grid(row=0, column=0, sticky=W, pady=2)

        Button(self._frame, text='Main Menu', command=self._handle_prev).grid()

        # add extra controls/functionalities
        if self._curr_user.teacher:
            pass
