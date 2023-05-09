import sqlite3

class Database:
    def __init__(self, path: str = "backend.db"):
        self._conn = sqlite3.connect(path)
        self._conn.isolation_level = None
        self._create_scheme()

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

    def execute(self, sql: str, params: tuple):
        cur = self._conn.cursor()
        cur.execute(sql, params)

        return cur.lastrowid

    def fetchone(self, sql:str, params: tuple):
        return self._conn.execute(sql, params).fetchone()

    def fetchall(self, sql:str, params: tuple):
        return self._conn.execute(sql, params).fetchall()

db = Database()
