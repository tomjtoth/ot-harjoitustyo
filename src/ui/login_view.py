import re
from textwrap import dedent
from tkinter import messagebox, Entry, Button, Label, W
from ui.common import View
from ui.prompt_text import PromptText
from backend.user_mgmt import user_mgr, WrongPassword


class LoginView(View):
    """1st view, used for authentication
    """

    def __init__(self, master, menu_view: callable):
        """Creates the view
        """
        super().__init__(master, menu_view, master.quit)
        self._create_widgets()
        self._re_user = re.compile(r"^[a-zA-Z_]\w{2,}$")
        self._re_pass = re.compile(r"^\w{8,16}$")

    def _create_widgets(self):
        """Populates the widgets in the view
        """
        Label(self._frame, text="username:").grid(
            row=0, column=0, sticky=W, pady=2)
        self._user = Entry(self._frame)
        self._user.grid(row=0, column=1, pady=2)
        self._user.focus_set()

        Label(self._frame, text="password:").grid(
            row=1, column=0, sticky=W, pady=2)
        self._pass = Entry(self._frame, show="*")
        self._pass.grid(row=1, column=1, pady=2)
        self._pass.bind("<Return>", lambda _event: self._process_input())

        Button(self._frame, text="Login/register",
               command=self._process_input).grid(columnspan=2)
        Button(self._frame, text="Quit",
               command=self._handle_prev).grid(columnspan=2)

    def _process_input(self):
        """Checking user input and trying to log in
        """
        username = self._user.get()
        password = self._pass.get()

        if not self._re_user.match(username):
            messagebox.showerror(
                "invalid username", dedent("""
                usernames should:
                - be more than 3 chars
                - contain only chars from class [a-zA-Z0-9_]
                - not begin with a digit [0-9]
                """))
            return

        if not self._re_pass.match(password):
            messagebox.showerror(
                "invalid password", dedent("""
                passwords should:
                - be between 8 and 16 chars
                - contain only chars from class [a-zA-Z0-9_]
                """))
            return

        try:
            user_mgr.login_register(username, password, self.pw_confirmation)
            self._handle_next()

        except WrongPassword as err:
            messagebox.showerror(*err.args)

    def pw_confirmation(self):
        """dwg_mgr forces the user to re-type the pw again upon registration

        Returns:
            str: the user password
        """
        return PromptText(self._master,
                          f"Registering {self._user.get()}",
                          {"text": "repeat password: "},
                          {"show": "*"},
                          {"text": "Confirm user creation"}
                          ).get()
