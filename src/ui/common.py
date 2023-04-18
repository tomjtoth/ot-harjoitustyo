from tkinter.ttk import Frame


class View:
    """Common for all views"""

    def __init__(self, master, next_view, prev_view):
        """Assigns the drawable frame"""

        self._master = master
        self._frame = Frame(master)
        self._handle_next = next_view
        self._handle_prev = prev_view

    def destroy(self):
        """Destroys the drawable frame"""

        self._frame.destroy()

    def show(self):
        """Shows the drawable frame"""

        self._frame.grid()
