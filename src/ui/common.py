from tkinter.ttk import Frame


class View:
    """Common for all views"""

    def __init__(self, master, next_view: callable, prev_view: callable):
        """Assigns the drawable frame"""

        self._master = master
        self._frame = Frame(master)
        self._handle_next = next_view
        self._handle_prev = prev_view

        # this is not working as the active GUI Control captures the keypress
        # no Quality of Life impro here, then...
        # self._frame.bind("<Escape>", lambda _ev: self._handle_prev())

    def destroy(self):
        """Destroys the drawable frame"""

        self._frame.destroy()

    def show(self):
        """Shows the drawable frame"""

        self._frame.grid()
