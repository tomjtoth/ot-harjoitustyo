import unittest
from backend.backend import Backend, WrongPassword
from entities.user import User


class TestUserManagement(unittest.TestCase):
    def setUp(self):
        self.backend = Backend(":memory:")

    def test_login_register(self):
        # register teacher
        self.backend.login_register("teacher", "teacher", True)
        teacher = self.backend.get_curr_user()
        self.assertEqual(('teacher', True), (teacher.name, teacher.teacher))

        # login works for teacher
        self.backend.login_register("teacher", "teacher")

        # login raises WronPassword for teacher
        self.assertRaises(
            WrongPassword, self.backend.login_register, "teacher", "wrong_pw")

        # register student
        self.backend.login_register("student", "student")
        student = self.backend.get_curr_user()
        self.assertEqual(('student', False), (student.name, student.teacher))

        # login works for student
        self.backend.login_register("student", "student")

        # login raises WronPassword for student
        self.assertRaises(
            WrongPassword, self.backend.login_register, "student", "wrong_pw")

class TestDrawing(unittest.TestCase):
    def setUp(self):
        self.backend = Backend(":memory:")
        self.backend.login_register("user", "user")

    def test_drawing(self):
        "ésu disable gnome-keyring daemon.{service,socket}"
