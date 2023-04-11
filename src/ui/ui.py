from ui.login import Login
from ui.drawing import Drawing
from ui.menu import Menu

from database.backend import Backend

class Ui:
    def __init__(self, master):
        self._master = master
        self._curr_view = None
        self.show_login()

    def show_login(self):
        self._destroy_curr()
        self._curr_view = Login(self._master, self.show_menu)
        self._curr_view.show()

    def show_menu(self):
        self._destroy_curr()
        self._curr_view = Menu(self._master, self.show_drawing, self.show_login)
        self._curr_view.show()

    def show_drawing(self):
        self._destroy_curr()
        self._curr_view = Drawing(self._master, self.show_menu)
        self._curr_view.show()

    def _destroy_curr(self):
        if self._curr_view:
            self._curr_view.destroy()
            self._curr_view = None
        

    

    
