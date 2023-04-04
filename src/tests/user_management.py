import unittest, os
from database.database import create_scheme, login_register, db, DB_PATH


class TestUserManagement(unittest.TestCase):
    def setUp(self):
        os.unlink(DB_PATH)
        create_scheme()
    
    def test_login_register(self):
        # registration
        self.assertEqual(True, login_register("root", "toor", True))

        # right pw
        self.assertEqual(True, login_register("root", "toor"))

        # wrong pw
        self.assertEqual(False, login_register("root", "wrong_pw"))