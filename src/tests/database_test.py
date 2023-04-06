import unittest
import os
from database.database import Backend


class TestUserManagement(unittest.TestCase):
    def setUp(self):
        self.db = Backend(":memory:")
        self.db.create_scheme()

    def test_login_register(self):
        # register teacher
        self.assertEqual((True, True), self.db.login_register(
            "teacher", "teacher", True))

        # right pw teacher
        self.assertEqual(
            (True, True), self.db.login_register("teacher", "teacher"))

        # wrong pw teacher
        self.assertEqual(
            (False, True), self.db.login_register("teacher", "wrong_pw"))

        # register student
        self.assertEqual(
            (True, False), self.db.login_register("student", "student"))

        # right pw student
        self.assertEqual(
            (True, False), self.db.login_register("student", "student"))

        # wrong pw student
        self.assertEqual(
            (False, False), self.db.login_register("student", "wrong_pw"))
