import sqlite3
import os

# TODO: get rid of wrappers and rebase Database(SQLite.connection) somehow


class Database:
    """Connection to the backend
    """

    def __init__(self, path: str):
        """Creates the connection

        Args:
            path (str): ':memory:' is used during testing
        """
        self._conn = sqlite3.connect(path)
        self._conn.isolation_level = None
        self._create_scheme()

    def _create_scheme(self):
        """Creates tables in DB if they don't exist already
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
            width integer not null,
            height integer not null,

            -- JSON
            content text not null
        );

        create table if not exists templates(
            drawing_id integer primary key references drawings(id)
        );
        """)

    def execute(self, sql: str, params: tuple) -> int:
        """wrapper for sqlite.conn.execute

        Args:
            sql (str): SQL to execute
            params (tuple): positional parameters

        Returns:
            int: last row ID
        """
        cur = self._conn.cursor()
        cur.execute(sql, params)
        return cur.lastrowid

    def fetchone(self, sql: str, params: tuple) -> tuple:
        """wrapper for sqlite.conn.fetchone

        Args:
            sql (str): SQL to execute
            params (tuple): positional parameters

        Returns:
            tuple: one row for the query
        """
        return self._conn.execute(sql, params).fetchone()

    def fetchall(self, sql: str, params: tuple) -> tuple:
        """wrapper for sqlite.conn.fetchall

        Args:
            sql (str): SQL to execute
            params (tuple): positional parameters

        Returns:
            tuple: all rowse for the query
        """
        return self._conn.execute(sql, params).fetchall()


db = Database(":memory:" if os.environ.get("TESTING") else "backend.db")
