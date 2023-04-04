import sqlite3, hashlib

DB_PATH = "backend.db"

db = sqlite3.connect(DB_PATH)
db.isolation_level = None


def create_scheme():
    """
        nothing special, simply creating the scheme
    """
    db.executescript("""
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
        name text not null,
        svg_data text not null, --or blob, idk yet, no idea what SVG libs are available in python...
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
def login_register(username: str, password: str, teacher: bool = False):
    """
    password should be passed as plain text, hashing happens within this func
    3rd argument only used during registration

    returns 2 booleans:
        - login/register succeess
        - user has teacher role
    """
    
    # storing pw as md5sum BAD IDEA!!!!
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    db_pass, db_role, _ = db.execute("""
    select password, iif(t.user_id, 1, 0) as role
    from users u
    left join teachers t on t.user_id == u.id
    where username=?""", [username]).fetchone()
    
    # user exists
    if db_pass:
        if password != db_pass:
            # wrong password
            return False, bool(db_role)
    
    # user does not exist, registering here
    else:
        lastrow = db.execute("insert into users(username, password) values (?, ?)"
            , [username, password])
        
        if teacher:
            db.execute("insert into teachers values(?)",[lastrow])
    
    # either login or register succeeded
    return True, bool(db_role)

def create_drawing():
    pass

def save_drawing():
    pass

