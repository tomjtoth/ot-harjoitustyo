from ui.login_view import LoginView
from ui.drawing_view import DrawingView
from ui.menu_view import MenuView


class Ui:
    """GUI used to navigate the app"""

    def __init__(self, master):
        """creates the GUI"""

        self._master = master
        self._curr_view = None

    def show_login(self):
        """changes to the login/register view"""

        self._change_view(LoginView(self._master, self.show_menu))

    def show_menu(self):
        """the user can select their old/new drawings from here"""

        self._change_view(
            MenuView(self._master, self.show_drawing, self.show_login))

    def show_drawing(self):
        """manipulating the drawing takes place here"""

        self._change_view(DrawingView(self._master, self.show_menu))

    def _change_view(self, next_view):
        """internal function that takes care of switching between the 3 main views"""

        if self._curr_view:
            self._curr_view.destroy()

        self._curr_view = next_view
        self._curr_view.show()
