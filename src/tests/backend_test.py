import unittest
import os
from entities.drawing import Drawing

# TESTING must be set before importing either user_mgr or dwg_mgr
os.environ.setdefault("TESTING", "setting this here for Backend")

from backend.dwg_mgmt import dwg_mgr, RECTANGLE, OVAL, LINE, TEXT
from backend.user_mgmt import user_mgr, WrongPassword

# needed because these tests build on top of each other, test order is strict
unittest.TestLoader.sortTestMethodsUsing = None


class DummyEvent:
    """mimicking user clicks to tkinter.Canvas"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def dummy_callback():
    """Backend._draw() spams the undo button into NORMAL state
    """


class DummyCanvas:
    """Backend._draw(...) heavily integrates with tkinter.Canvas
       These methods are called during normal operation
       I only need to check on the logging capability of my Drawing
    """

    def create_rectangle(self, *args, **kwargs):
        pass

    def create_oval(self, *args, **kwargs):
        pass

    def create_line(self, *args, **kwargs):
        pass

    def create_text(self, *args, **kwargs):
        pass


class TestUserLoginRegister(unittest.TestCase):
    def test_login_register_teacher(self):

        user_mgr.login_register("teacher", "teacher", lambda: "teacher", True)
        teacher = user_mgr.get_curr_user()
        self.assertEqual(("teacher", True), (teacher.name, teacher.teacher))

        # login works
        user_mgr.login_register("teacher", "teacher")

        # login raises WrongPassword
        self.assertRaises(
            WrongPassword, user_mgr.login_register, "teacher", "wrong_pw")

    def test_login_register_student(self):
        user_mgr.login_register("student", "student", lambda: "student")
        student = user_mgr.get_curr_user()
        self.assertEqual(("student", False), (student.name, student.teacher))

        # login works
        user_mgr.login_register("student", "student")

        # login raises WrongPassword
        self.assertRaises(
            WrongPassword, user_mgr.login_register, "student", "wrong_pw")


class TestDrawing(unittest.TestCase):
    def setUp(self):
        user_mgr.login_register("student", "student")
        self.test_features = (
            (OVAL, "purple", "black"),
            (RECTANGLE, "green", "yellow"),
            (LINE, "blue", "gray"),
            (TEXT, "red", "white"))
        self.test_ev1 = DummyEvent(20, 20)
        self.test_ev2 = DummyEvent(100, 100)

    def test_0_save_new_dwg_complex(self):
        dwg_mgr.set_curr_dwg(
            Drawing("4 features at 20,20,100,100", 640, 480))
        dwg_mgr.set_canvas(DummyCanvas(), dummy_callback)

        # adding 4 features
        for (cmd, fill, border) in self.test_features:
            dwg_mgr.set_cmd(cmd)
            dwg_mgr.set_fill(fill)
            dwg_mgr.set_border(border)

            # emulate user clicks
            if cmd == TEXT:
                dwg_mgr.b1_up(self.test_ev2, "testi teksti")
            else:
                dwg_mgr.b1_dn(self.test_ev1)
                dwg_mgr.b1_up(self.test_ev2)

        dwg_mgr.save_curr_dwg()

    def test_1_dwg_content_intact(self):
        dwg = dwg_mgr.get_user_dwgs(user_mgr.get_curr_user().id)[0]

        self.assertTupleEqual(
            ("4 features at 20,20,100,100", 640, 480),
            (dwg.name, dwg.width, dwg.height))

        i = 0
        for (cmd, coords, kwargs) in dwg.reproduce():
            # 1 color for LINE, 2 colors for the other 3 features
            if i < 4:
                # the last TEXT in the self.test_features actually creates 2 entries
                orig_cmd, *orig_clrs = self.test_features[i]

            self.assertEqual(cmd, orig_cmd)

            # OVAL, RECTANGLE, LINE
            if len(coords) == 4:
                self.assertListEqual(coords,
                                     [self.test_ev1.x, self.test_ev1.y,
                                      self.test_ev2.x, self.test_ev2.y])

                if cmd == LINE:
                    self.assertDictEqual(kwargs,
                                         {"fill": orig_clrs[0], "width": 10})
                else:
                    self.assertDictEqual(kwargs,
                                         {"fill": orig_clrs[0],
                                          "outline": orig_clrs[1],
                                          "width": 10})

            # TEXT
            else:
                self.assertIn(coords,
                              ([self.test_ev1.x, self.test_ev1.y],
                               [self.test_ev2.x, self.test_ev2.y]))
                self.assertEqual(kwargs["text"], "testi teksti")

            i += 1

    def test_2_user_cannot_see_others_dwgs(self):
        # this is a completely new user who has no drawings
        user_mgr.login_register("user2", "user2", lambda: "user2")

        # user1 has 1 dwg in the DB at this point, but user2 shall not see it
        self.assertEqual(len(dwg_mgr.get_user_dwgs(
            user_mgr.get_curr_user().name)), 0)

    def test_3_dwg_undo_redo_works(self):
        pass