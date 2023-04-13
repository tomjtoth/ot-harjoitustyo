from ui.login_view import LoginView
from ui.drawing_view import DrawingView
from ui.menu_view import MenuView


class Ui:
    def __init__(self, master):
        self._master = master
        self._curr_view = None

    def show_login(self):
        self._change_view(LoginView(self._master, self.show_menu))

    def show_menu(self):
        self._change_view(
            MenuView(self._master, self.show_drawing, self.show_login))

    def show_drawing(self, dwg):
        self._change_view(DrawingView(self._master, self.show_menu, dwg))

    def _change_view(self, next_view):
        if self._curr_view:
            self._curr_view.destroy()

        self._curr_view = next_view
        self._curr_view.show()
