from tkinter.ttk import Frame


class View:
    """Common for all views
    """

    def __init__(self, master, next_view: callable, prev_view: callable):
        """Creates a drawable frame

        Args:
            master (tkinter.root): 
            next_view (callable): handle for goind forward
            prev_view (callable): handle for going backwards
        """
        self._master = master
        self._frame = Frame(master)
        self._handle_next = next_view
        self._handle_prev = prev_view

    def destroy(self):
        """Destroys the drawable frame
        """
        self._frame.destroy()

    def show(self):
        """Shows the drawable frame
        """
        self._frame.grid()
