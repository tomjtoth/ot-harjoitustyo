import sqlite3
import os


conn = sqlite3.connect(
    ":memory:" if os.environ.get("TESTING") else "backend.db")
conn.isolation_level = None

conn.executescript("""
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
