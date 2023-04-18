class User:
    """user with the optional teacher role"""

    def __init__(self, user_id: int, username: str, teacher: bool = False):
        """builds a User"""

        self.id = user_id
        self.name = username
        self.teacher = teacher
