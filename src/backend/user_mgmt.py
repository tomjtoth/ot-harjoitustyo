import hashlib
from entities.user import User
from backend.database import conn


class WrongPassword(Exception):
    """Thrown when authentication fails

    Args:
        list: title and message to show
    """


class UserManager:
    """Handles authentication
    """

    def __init__(self):
        """Creates the manager
        """
        self._curr_user = None
        self._conn = conn

    def login_register(self,
                       username: str,
                       password: str,
                       pw_conf: callable,
                       teacher: bool = False):
        """Unified method to login/register users

        Args:
            username (str)
            password (str): passed as plain text, hashing happens within this method
            pw_conf (callable): used only upon registration
            teacher (bool, optional): for future reference

        Returns:
            None

        Raises:
            WrongPassword
        """

        # storing pw as md5sum BAD IDEA!!!!
        pw_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
        db_res = self._conn.execute("""
        select u.id, password, iif(t.user_id, 1, 0) as role
        from users u
        left join teachers t on t.user_id == u.id
        where username=?""", (username, )).fetchone()

        # user exists
        if db_res:
            if pw_hash != db_res[1]:
                raise WrongPassword("Login failed", "Wrong password")
            user_id = db_res[0]
            teacher = bool(db_res[2])

        # user does not exist, registering here
        else:
            if password != pw_conf():
                raise WrongPassword("Registration failed",
                                    "Passwords don't match")

            cur = self._conn.cursor()
            user_id = cur.execute(
                "insert into users(username, password) values (?, ?)",
                (username, pw_hash)).lastrowid

            if teacher:
                self._conn.execute(
                    "insert into teachers values(?)", (user_id, ))

        self._curr_user = User(user_id, username, teacher)

    def get_curr_user(self):
        """Retreives the currently logged in user
        """
        return self._curr_user


user_mgr = UserManager()
