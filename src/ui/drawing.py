from tkinter import messagebox, Tk, Listbox, Button, Label, W
from ui.common import View

class Drawing(View):
    """drawing view"""

    def __init__(self, master, menu_view):
        """creates the main drawing view"""

        super().__init__(master, None, menu_view)
        self._create_widgets()
    
    def _create_widgets(self):
        Label(self._frame, text='You\'re logged in as XY').grid(
            row=0, column=0, sticky=W, pady=2)

        Button(self._frame, text='Main Menu', command=self._handle_prev).grid()
        
