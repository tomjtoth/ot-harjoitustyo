import unittest, os
from database.database import create_scheme, login_register, db, DB_PATH


class TestUserManagement(unittest.TestCase):
    def setUp(self):
        create_scheme()
    
    def test_login_register(self):
        # registration
        self.assertEqual((True, True), login_register("root", "toor", True))

        # right pw
        self.assertEqual((False, True), login_register("root", "toor"))

        # wrong pw
        self.assertEqual((False, False), login_register("root", "wrong_pw"))