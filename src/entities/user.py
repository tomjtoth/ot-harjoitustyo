class User:
    "user with the optional teacher role"

    def __init__(self, id: int, username: str, teacher: bool = False):
        "builds a User"

        self.id = id
        self.name = username
        self.teacher = teacher
