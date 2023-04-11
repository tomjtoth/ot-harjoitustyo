from ui.common import View

class Drawing(View):
    """drawing view"""

    def __init__(self, master, menu_view):
        """creates the main drawing view"""
        super().__init__(master, None, menu_view)