import unittest
import os

# TESTING must be set before importing either user_mgr or dwg_mgr
os.environ.setdefault("TESTING", "setting this here for Backend")

# pylint: disable=wrong-import-position
from backend.user_mgmt import user_mgr, WrongPassword


# needed because these tests build on top of each other, test order is strict
unittest.TestLoader.sortTestMethodsUsing = None


class Test0TeacherRegister(unittest.TestCase):
    def test_0_wrong_pw_raises(self):
        self.assertRaises(WrongPassword,
            user_mgr.login_register, "teacher", "teacher", lambda: "NOT TEACHER", True)

    def test_1_right_pw_passes(self):
        user_mgr.login_register("teacher", "teacher", lambda: "teacher", True)
        teacher = user_mgr.get_curr_user()
        self.assertEqual(("teacher", True), (teacher.name, teacher.teacher))


class Test1TeacherLogin(unittest.TestCase):
    def test_0_wrong_pw_raises(self):
        self.assertRaises(
            WrongPassword, user_mgr.login_register, "teacher", "NOT TEACHER", lambda: None)

    def test_1_right_pw_passes(self):
        user_mgr.login_register("teacher", "teacher", lambda: None)
        teacher = user_mgr.get_curr_user()
        self.assertEqual(("teacher", True), (teacher.name, teacher.teacher))


class Test2StudentRegister(unittest.TestCase):
    def test_0_wrong_pw_raises(self):
        self.assertRaises(WrongPassword,
            user_mgr.login_register, "student", "student", lambda: "NOT STUDENT")

    def test_1_right_pw_passes(self):
        user_mgr.login_register("student", "student", lambda: "student")
        student = user_mgr.get_curr_user()
        self.assertEqual(("student", False), (student.name, student.teacher))


class Test3StudentLogin(unittest.TestCase):
    def test_0_wrong_pw_raises(self):
        self.assertRaises(
            WrongPassword, user_mgr.login_register, "student", "NOT STUDENT", lambda: None)

    def test_1_right_pw_passes(self):
        user_mgr.login_register("student", "student", lambda: None)
        student = user_mgr.get_curr_user()
        self.assertEqual(("student", False), (student.name, student.teacher))
