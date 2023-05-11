from ui.login_view import LoginView
from ui.drawing_view import DrawingView
from ui.menu_view import MenuView


class Ui:
    """GUI used to navigate the app
    """

    def __init__(self, master):
        """creates the GUI
        """
        self._master = master
        self._curr_view = None

    def show_login(self):
        """Transition TO 1st view
        """
        self._change_view(
            LoginView(self._master, self.show_menu))

    def show_menu(self):
        """Transition TO 2nd view
        """
        self._change_view(
            MenuView(self._master, self.show_drawing, self.show_login))

    def show_drawing(self):
        """Transition TO 3rd view
        """
        self._change_view(
            DrawingView(self._master, self.show_menu))

    def _change_view(self, next_view: callable):
        """Destroys current and sets next view
        """
        if self._curr_view:
            self._curr_view.destroy()

        self._curr_view = next_view
        self._curr_view.show()
