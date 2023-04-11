class User:
    def __init__(self, username, password, teacher):
        self.username = username
        self.__password = password
        self.teacher = teacher
