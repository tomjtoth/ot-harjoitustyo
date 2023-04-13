import sqlite3
import hashlib

from entities.user import User


class WrongPassword(Exception):
    pass


class Backend:
    """
        takes care of literally EVERYTHING, will break it up later once everything works.....
    """

    def __init__(self, path: str = "backend.db"):
        "path can be overridden for testing purposes, e.g. ':memory:'"

        self._path = path
        self._conn = sqlite3.connect(path)
        self._conn.isolation_level = None
        self._curr_user = None
        self.create_scheme()

    def create_scheme(self):
        """
            nothing special, simply creating the scheme
        """
        self._conn.executescript("""
        create table if not exists users(
            id integer primary key,
            username text not null,
            
            --stored as md5sum, never gonna do it in PROD, pinky-promise
            password text not null
        );
        
        create table if not exists teachers(
            user_id integer primary key references users(id)
        );

        create table if not exists drawings(
            id integer primary key,
            owner_id integer references users(id),
            name text not null,
            svg_data text not null --or blob, idk yet, no idea what SVG libs are available in python...
        );

        create table if not exists templates(
            drawing_id integer primary key references drawings(id)
        );
        """)

    # just 1 button, no time for 2 different methodzzZZzz
    def login_register(self, username: str, password: str, teacher: bool = False):
        """
        password should be passed as plain text, hashing happens within this func
        3rd argument is only used during registration
        """

        # storing pw as md5sum BAD IDEA!!!!
        password = hashlib.md5(password.encode('utf-8')).hexdigest()
        db_res = self._conn.execute("""
        select u.id, password, iif(t.user_id, 1, 0) as role
        from users u
        left join teachers t on t.user_id == u.id
        where username=?""", [username]).fetchone()

        # user exists
        if db_res:

            if password != db_res[1]:
                raise WrongPassword
            
            id = db_res[0]
            teacher = bool(db_res[2])

        # user does not exist, registering here
        else:
            cur = self._conn.cursor()
            cur.execute("insert into users(username, password) values (?, ?)", [
                        username, password])

            id = cur.lastrowid

            if teacher:
                self._conn.execute("insert into teachers values(?)", [id])

        # either login or register succeeded
        self._curr_user = User(id, username, teacher)

    def get_curr_user(self):
        return self._curr_user

    def get_user_dwgs(self):
        arr = []
        for x in self._conn.execute("""
        select name, iif(t.owner_id, 1, 0) as template
        from drawings d
        left join templates t on t.drawing_id == d.id
        left join 
        where username=?
        """).fetchall():
            pass
        return arr

    def create_drawing(self):
        pass

    def save_drawing(self):
        pass


backend = Backend()
