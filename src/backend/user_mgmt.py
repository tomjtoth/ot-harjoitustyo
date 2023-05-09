import hashlib
from entities.user import User
from backend.database import db

class WrongPassword(Exception):
    pass

class UserManager:
    """Handles authentication"""

    def __init__(self):
        """Constructor"""

        self._curr_user = None
        self._conn = db

    def login_register(self,
        username: str,
        password: str,
        pw_conf: callable,
        teacher: bool = False):
        """Unified method to login/register users

        Args:
            username (str)
            password (str): passed as plain text
            pw_conf (callable): used upon registration
            teacher (bool, optional): for future reference

        Returns:
            None

        Raises:
            WrongPassword
        """

        # storing pw as md5sum BAD IDEA!!!!
        pw_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        db_res = self._conn.fetchone("""
        select u.id, password, iif(t.user_id, 1, 0) as role
        from users u
        left join teachers t on t.user_id == u.id
        where username=?""", (username, ))

        # user exists
        if db_res:

            if pw_hash != db_res[1]:
                raise WrongPassword

            user_id = db_res[0]
            teacher = bool(db_res[2])

        # user does not exist, registering here
        else:
            if password != pw_conf():
                raise WrongPassword

            user_id = self._conn.execute(
                "insert into users(username, password) values (?, ?)",
                (username, pw_hash))

            if teacher:
                self._conn.execute(
                    "insert into teachers values(?)", (user_id, ))

        # either login or register succeeded
        self._curr_user = User(user_id, username, teacher)

    def get_curr_user(self):
        """retreives the currently logged in user"""

        return self._curr_user

user_mgr = UserManager()
