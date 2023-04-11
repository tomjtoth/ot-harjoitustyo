from tkinter import messagebox, Tk, Listbox, Button, Label, W
from ui.common import View

class Menu(View):
    """main menu view"""
    
    def __init__(self, master, drawing_view, login_view):
        """creates the main menu view"""

        super().__init__(master, drawing_view, login_view)
        self._create_widgets()

    def _create_widgets(self):
        Label(self._frame, text='You\'re logged in as XY').grid(
            row=0, column=0, sticky=W, pady=2)

        Button(self._frame, text='Let\'s draw!', command=self._handle_next).grid()
        Button(self._frame, text='Logout', command=self._handle_prev).grid()
        
    