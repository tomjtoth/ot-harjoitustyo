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
        self._create_scheme()

    def _create_scheme(self):
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
        
        --create at least 1 teacher
        -- toistuisi turhaan joka kertaa..
        -- WiP
        /*
        insert into users(username, password) values ('root', 'toor');
        insert into teachers values(1);
        */

        create table if not exists drawings(
            id integer primary key,
            name text not null,
            svg_data text not null --or blob, idk yet, no idea what SVG libs are available in python...
        );

        create table if not exists templates(
            drawing_id integer primary key references drawings(id)
        );
        create table if not exists ownership (
            drawing_id integer references drawings(id),
            user_id integer references users(id),

            --1 drawing can only belong to 1 user
            primary key (drawing_id, user_id)
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
        select password, iif(t.user_id, 1, 0) as role
        from users u
        left join teachers t on t.user_id == u.id
        where username=?""", [username]).fetchone()

        # user exists
        if db_res:

            teacher = bool(db_res[1])

            if password != db_res[0]:
                # wrong password
                raise WrongPassword

        # user does not exist, registering here
        else:
            cur = self._conn.cursor()
            cur.execute("insert into users(username, password) values (?, ?)", [
                        username, password])

            if teacher:
                self._conn.execute(
                    "insert into teachers values(?)", [cur.lastrowid])

        # either login or register succeeded
        self._curr_user = User(username, password, teacher)

    def get_curr_user(self):
        return self._curr_user

    def create_drawing(self):
        pass

    def save_drawing(self):
        pass


backend = Backend()
