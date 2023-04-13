import unittest
from backend.backend import Backend, WrongPassword
from entities.user import User


class TestUserManagement(unittest.TestCase):
    def setUp(self):
        self.backend = Backend(":memory:")
        self.backend.create_scheme()

    def test_login_register(self):
        # register teacher
        #self.assertRaises(None,
        #    self.backend.login_register("teacher", "teacher", True))
        self.assertEqual(User('teacher', True), self.backend.get_curr_user())

        # right pw teacher
        self.assertEqual(
            (True, True), self.backend.login_register("teacher", "teacher"))

        # wrong pw teacher
        self.assertRaises(WrongPassword, self.backend.login_register("teacher", "wrong_pw"))


        # register student
        self.assertEqual(
            (True, False), self.backend.login_register("student", "student"))

        # right pw student
        self.assertEqual(
            (True, False), self.backend.login_register("student", "student"))

        # wrong pw student
        self.assertEqual(
            (False, False), self.backend.login_register("student", "wrong_pw"))
