import unittest, os
from database.database import Backend


class TestUserManagement(unittest.TestCase):
    def setUp(self):
        db = Backend(":memory:")
        db.create_scheme()
    
    def test_login_register(self):
        # registration
        self.assertEqual((True, True), db.login_register("root", "toor", True))

        # right pw
        self.assertEqual((False, True), db.login_register("root", "toor"))

        # wrong pw
        self.assertEqual((False, False), db.login_register("root", "wrong_pw"))