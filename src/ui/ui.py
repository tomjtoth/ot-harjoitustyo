from ui.login import Login
from ui.drawing import Drawing
from ui.menu import Menu


class Ui:
    def __init__(self, master):
        self._master = master
        self._curr_view = None

    def show_login(self):
        self._change_view(Login(self._master, self.show_menu))

    def show_menu(self):
        self._change_view(
            Menu(self._master, self.show_drawing, self.show_login))

    def show_drawing(self):
        self._change_view(Drawing(self._master, self.show_menu))

    def _change_view(self, next_view):
        if self._curr_view:
            self._curr_view.destroy()

        self._curr_view = next_view
        self._curr_view.show()
