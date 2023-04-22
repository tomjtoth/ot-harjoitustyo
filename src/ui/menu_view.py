from tkinter import messagebox, Listbox, Button, Label, W, Toplevel, Entry, Label, StringVar, IntVar
from ui.common import View
from backend.backend import backend
from entities.drawing import Drawing


class MenuView(View):
    """shows a list of drawings available to the user"""

    def __init__(self, master, drawing_view, login_view):
        """creates the main menu view"""

        super().__init__(master, drawing_view, login_view)
        self._user = backend.get_curr_user()
        self._create_widgets()

    def _create_widgets(self):
        """internal func, creates all the GUI controls"""

        Button(
            self._frame, text=f"Logout ({self._user.name})", command=self._handle_prev).grid()

        self._dwgs = backend.get_user_dwgs()

        self._lb_dwg = Listbox(self._frame)
        self._lb_dwg.bind(
            '<Return>', lambda _event: self._proceed_to_next_view())
        self._lb_dwg.grid()
        self._lb_dwg.insert(0, '<NEW DRAWING>')

        # select 1st element
        self._lb_dwg.select_set(0)
        self._lb_dwg.event_generate("<<ListboxSelect>>")
        self._lb_dwg.focus_set()
        self._lb_dwg.bind('<Return>', lambda _ev: self._proceed_to_next_view())

        for i, dwg in enumerate(self._dwgs):
            self._lb_dwg.insert(i+1, dwg.name)

        Button(self._frame, text='Let\'s draw!',
               command=self._proceed_to_next_view).grid()

        # add extra controls/functionalities
        if self._user.teacher:
            pass

    def _proceed_to_next_view(self):
        """sets up a new or old drawing and proceeds to drawing view"""

        dwg_i = self._lb_dwg.curselection()[0]

        # should be separated to own module at some point..
        if dwg_i == 0:
            pop_up = Toplevel(self._frame)
            pop_up.title('New DWG')

            name = StringVar(pop_up, value='jotain uusi')
            Label(pop_up, text='name:').grid(column=0, row=0)
            Entry(pop_up, textvariable=name).grid(column=1, row=0)

            width = IntVar(pop_up, value=800)
            Label(pop_up, text='width:').grid(column=0, row=1)
            Entry(pop_up, textvariable=width).grid(column=1, row=1)

            height = IntVar(pop_up, value=600)
            Label(pop_up, text='height:').grid(column=0, row=2)
            Entry(pop_up, textvariable=height).grid(column=1, row=2)

            Button(pop_up, text='Create', command=lambda: self._new_dwg(name, width, height, pop_up.destroy)
                   ).grid(columnspan=2, row=3)

            pop_up.wait_window()

        else:
            backend.set_curr_dwg(self._dwgs[dwg_i-1])

        self._handle_next()

    def _new_dwg(self, name, width, height, killswitch):
        """helper method for setting up a new drawing"""

        backend.set_curr_dwg(Drawing(name.get(), width.get(), height.get()))
        killswitch()
