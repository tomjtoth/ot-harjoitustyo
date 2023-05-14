from tkinter import Listbox, Button
from ui.common import View
from ui.prompt_drawing import PromptDrawing
from backend.user_mgmt import user_mgr
from backend.dwg_mgmt import dwg_mgr
from entities.drawing import Drawing


class MenuView(View):
    """2nd view, shows drawings of given user
    """

    def __init__(self, master, drawing_view: callable, login_view: callable):
        """Creates the menu view
        """
        super().__init__(master, drawing_view, login_view)
        self._user = user_mgr.get_curr_user()
        self._create_widgets()

    def _create_widgets(self):
        """Populates the widgets in the view
        """
        Button(self._frame, text=f"Logout ({self._user.name})",
               command=self._handle_prev).grid()

        self._dwgs = dwg_mgr.get_user_dwgs(self._user.id)

        self._lb_dwg = Listbox(self._frame)
        self._lb_dwg.bind("<Return>",
                          lambda _event: self._proceed_to_next_view())
        self._lb_dwg.grid()
        self._lb_dwg.insert(0, "<NEW DRAWING>")

        # select 1st element
        self._lb_dwg.select_set(0)
        self._lb_dwg.event_generate("<<ListboxSelect>>")
        self._lb_dwg.focus_set()
        self._lb_dwg.bind("<Return>", lambda _ev: self._proceed_to_next_view())

        for i, dwg in enumerate(self._dwgs):
            self._lb_dwg.insert(i+1, dwg.name)

        Button(self._frame, text="Let's draw!",
               command=self._proceed_to_next_view).grid()

        # add extra controls/functionalities
        if self._user.teacher:
            pass

    def _proceed_to_next_view(self):
        """Additional preparations for the DrawingView
        """
        dwg_i = self._lb_dwg.curselection()[0]

        if dwg_i == 0:
            name, width, height = PromptDrawing(self._frame).get()
            dwg_mgr.set_curr_dwg(Drawing(name, width, height))
        else:
            dwg_mgr.set_curr_dwg(self._dwgs[dwg_i-1])

        self._handle_next()
