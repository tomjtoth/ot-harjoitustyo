class User:
    def __init__(self, username, password, teacher):
        self.name = username
        self.__pw = password
        self.teacher = teacher
