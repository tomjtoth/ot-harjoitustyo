from tkinter import messagebox, Listbox, Button, Label, W
from ui.common import View
from backend.backend import backend
from entities.drawing import Drawing

class MenuView(View):
    """main menu view"""

    def __init__(self, master, drawing_view, login_view):
        """creates the main menu view"""

        super().__init__(master, drawing_view, login_view)
        self._user = backend.get_curr_user()
        self._create_widgets()

    def _create_widgets(self):
        Label(self._frame, text=f"Login: {self._user.name}").grid(row=0, column=0, sticky=W, pady=2)

        
        self._dwgs = [] #backend.get_user_dwgs()

        self.lb_dwg = Listbox(self._frame)
        self.lb_dwg.insert(0, '<NEW DRAWING>')
        self.lb_dwg.grid()
        
        Button(self._frame, text='Let\'s draw!',
               command=self._proceed_to_next_view).grid()
        Button(self._frame, text='Logout', command=self._handle_prev).grid()

        # add extra controls/functionalities
        if self._user.teacher:
            pass

    def _proceed_to_next_view(self):
        dwg_i = self.lb_dwg.curselection()[0]
        if dwg_i == 0:
            dwg = Drawing('hardcoded new name')

        self._handle_next(dwg)
