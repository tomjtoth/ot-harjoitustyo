import sqlite3
import hashlib
import json
from collections import deque
from entities.user import User
from entities.drawing import Drawing

RECTANGLE = 0
OVAL = 1
LINE = 2
TEXT = 3


class WrongPassword(Exception):
    pass


class Backend:
    """
        takes care of literally EVERYTHING,
        will break it up later once everything works.....
    """

    # pylint: disable=too-many-instance-attributes
    # I need all of them!

    def __init__(self, path: str = "backend.db"):
        """path can be overridden for testing purposes, e.g. ':memory:'"""

        self._conn = sqlite3.connect(path)
        self._conn.isolation_level = None
        self._curr_user = None
        self._curr_dwg = None
        self._create_scheme()

        self._clicks = 0
        self._curr_cmd = RECTANGLE
        self._text_prompter = None
        self._curr_fill = 'red'
        self._curr_border = 'green'
        self._coords = deque()
        self._canvas = None

    def _create_scheme(self):
        """creating scheme on 1st run, no-op later.."""

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
            width integer not null,
            height integer not null,
            
            -- JSON
            content text not null
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
        where username=?""", (username, )).fetchone()

        # user exists
        if db_res:

            if password != db_res[1]:
                raise WrongPassword

            user_id = db_res[0]
            teacher = bool(db_res[2])

        # user does not exist, registering here
        else:
            cur = self._conn.cursor()
            cur.execute(
                "insert into users(username, password) values (?, ?)",
                (username, password))

            user_id = cur.lastrowid

            if teacher:
                self._conn.execute(
                    "insert into teachers values(?)", (user_id, ))

        # either login or register succeeded
        self._curr_user = User(user_id, username, teacher)

    def get_curr_user(self):
        """retreives the currently logged in user"""

        return self._curr_user

    def get_user_dwgs(self):
        return [
            Drawing(name, width, height, dwg_id, json.loads(content))
            for name, width, height, dwg_id, content
            in self._conn.execute("""
            select name, width, height, id, content
            from drawings d
            where owner_id=?
            """, (self._curr_user.id, )).fetchall()
        ]

    def save_curr_dwg(self):
        """stores python's Drawing's content to SQLite in JSON"""

        # existing drawing
        if self._curr_dwg.id:
            self._conn.execute("""
            update drawings set content = ?
            where id = ?
            """, (self._curr_dwg.stringify(), self._curr_dwg.id))

        # new drawing
        else:
            self._conn.execute("""
            insert into drawings(
                owner_id,
                name,
                width,
                height,
                content
            ) values (?,?,?,?,?)
            """, (
                self._curr_user.id,
                self._curr_dwg.name,
                self._curr_dwg.width,
                self._curr_dwg.height,
                self._curr_dwg.stringify()
            ))

    def get_curr_dwg(self):
        """gets the current drawing"""
        return self._curr_dwg

    def set_curr_dwg(self, dwg):
        """assigns the current drawing to backend"""

        self._curr_dwg = dwg

    def set_canvas(self, canvas):
        """assigns the current canvas to backend"""

        self._canvas = canvas
        for (feature, coords, kwargs) in self._curr_dwg.reproduce():
            self._draw(feature, *coords, logging=False, **kwargs)

    def set_cmd(self, cmd):
        """sets the currently initiated command"""

        self._curr_cmd = cmd

    def set_text_prompter(self, prompt):
        """Makes backend able to call a pop-up window for querying the text"""

        self._text_prompter = prompt

    def set_fill(self, color):
        """sets the fill color"""

        self._curr_fill = color

    def set_border(self, color):
        """sets the border color"""

        self._curr_border = color

    def _draw(self, cmd, *args, logging=True, **kwargs):
        """creates features on the current canvas + stores recipie in drawing's log"""

        if cmd == RECTANGLE:
            self._canvas.create_rectangle(*args, **kwargs)

        elif cmd == OVAL:
            self._canvas.create_oval(*args, **kwargs)

        elif cmd == LINE:
            self._canvas.create_line(*args, **kwargs)

        elif cmd == TEXT:
            self._canvas.create_text(*args, **kwargs)

        if logging:
            self._curr_dwg.add(cmd, *args, **kwargs)

    # placeholder atm
    def b1_dn(self, event):
        """left button pressed"""

    def b1_up(self, event, test_helper=None):
        """left button released"""

        self._coords.append(event.x)
        self._coords.append(event.y)

        # keeping track of 2 (x,y) coords
        while len(self._coords) > 4:
            self._coords.popleft()

        if self._curr_cmd == TEXT:

            self._draw(self._curr_cmd, self._coords[-2], self._coords[-1],
                       text=test_helper if test_helper else self._text_prompter(),
                       fill=self._curr_fill)

        else:
            self._clicks += 1

            if self._clicks % 2 == 0:
                if self._curr_cmd == LINE:
                    self._draw(self._curr_cmd, *self._coords,
                               fill=self._curr_fill, width=10)
                else:
                    self._draw(self._curr_cmd, *self._coords,
                               outline=self._curr_border, fill=self._curr_fill, width=10)

    # jatkokehari?
    def b1_mv(self, event):
        """dragged while left button pressed"""


# exporting this one here
backend = Backend()
