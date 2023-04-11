import re
from textwrap import dedent
from tkinter import messagebox, Tk, Entry, Button, Label, W
from ui.common import View
from services.login_manager import LoginManager

class Login(View):
    """Makes logging in possible via GUI"""

    def __init__(self, master, menu_view):
        """creates the view"""
        super().__init__(master, menu_view, master.quit)
        self._create_widgets()
        self._re_user = re.compile(r"^[a-zA-Z_]\w{2,}$")
        self._re_pass = re.compile(r"^\w{8,16}$")

    def _create_widgets(self):
        Label(self._frame, text='username:').grid(
            row=0, column=0, sticky=W, pady=2)
        self._user = Entry(self._frame)
        self._user.grid(row=0, column=1, pady=2)

        Label(self._frame, text='password:').grid(
            row=1, column=0, sticky=W, pady=2)
        self._pass = Entry(self._frame, show="*")
        self._pass.grid(row=1, column=1, pady=2)

        Button(self._frame, text='Login/register',
                  command=self._process_input).grid(columnspan=2)
        Button(self._frame, text='Quit', command=self._handle_prev).grid(columnspan=2)

    def _process_input(self):
        username = self._user.get()
        password = self._pass.get()

        if not self._re_user.match(username):
            messagebox.showerror(
                "invalid username", dedent("""
                usernames should:
                - be more than 3 chars
                - contain only chars from a-zA-Z0-9_
                """))
            return

        if not self._re_pass.match(password):
            messagebox.showerror(
                "invalid password", dedent("""
                passwords should:
                - be between 8 and 16 chars
                - contain only chars from a-zA-Z0-9_
                """))
            return

        try:
            self._handle_next()
            return
            teacher = self.backend.login_register(
            username, password)
            messagebox.showinfo(
                "Succeess", f"you're in!{' ... as a teacher' if teacher else ''}")

        except:
            messagebox.showerror("Login/register failed", "wrong password")
