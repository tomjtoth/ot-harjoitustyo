import unittest
import os
from uuid import uuid4
from backend.backend import Backend, WrongPassword, RECTANGLE, OVAL, LINE, TEXT
from entities.drawing import Drawing

# testing drawing related stuff requires a persistent DB
# meaning individual tests cannot be initiated, only in batches
TEST_DB = f"{uuid4()}_test.db"


class DummyEvent:
    """mimicking user clicks to tkinter.Canvas"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class DummyCanvas:
    """
        Backend._draw(...) heavily integrates with tkinter.Canvas
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
    def setUp(self):
        self.backend = Backend(TEST_DB)

    def test_login_register_teacher(self):
        self.backend.login_register("teacher", "teacher", True)
        teacher = self.backend.get_curr_user()
        self.assertEqual(('teacher', True), (teacher.name, teacher.teacher))

        # login works
        self.backend.login_register("teacher", "teacher")

        # login raises WrongPassword
        self.assertRaises(
            WrongPassword, self.backend.login_register, "teacher", "wrong_pw")

    def test_login_register_student(self):
        self.backend.login_register("student", "student")
        student = self.backend.get_curr_user()
        self.assertEqual(('student', False), (student.name, student.teacher))

        # login works
        self.backend.login_register("student", "student")

        # login raises WrongPassword
        self.assertRaises(
            WrongPassword, self.backend.login_register, "student", "wrong_pw")


class TestDrawing(unittest.TestCase):
    def setUp(self):
        self.backend = Backend(TEST_DB)
        self.backend.login_register("user1", "user1")

        self.test_features = (
            (OVAL, 'purple', 'black'),
            (RECTANGLE, 'green', 'yellow'),
            (LINE, 'blue', 'gray'),
            (TEXT, 'red', 'white'))
        self.test_ev1 = DummyEvent(20, 20)
        self.test_ev2 = DummyEvent(100, 100)

    def test_0_save_new_drawing_complex(self):
        """
            ilmeisesti näitä käynnistetään AAKKOSISSA..
            siksi _0_ tagi..
        """
        self.backend.set_curr_dwg(
            Drawing("4 features at 20,20,100,100", 640, 480))
        self.backend.set_canvas(DummyCanvas())

        # adding 4 features
        for (cmd, fill, border) in self.test_features:
            self.backend.set_cmd(cmd)
            self.backend.set_fill(fill)
            self.backend.set_border(border)

            # emulate user clicks
            if cmd == TEXT:
                self.backend.b1_up(self.test_ev2, "testi teksti")
            else:
                self.backend.b1_up(self.test_ev1)
                self.backend.b1_up(self.test_ev2)

        self.backend.save_curr_dwg()

    def test_1_dwg_content_intact(self):
        dwg = self.backend.get_user_dwgs()[0]

        self.assertTupleEqual(
            ("4 features at 20,20,100,100", 640, 480),
            (dwg.name, dwg.width, dwg.height))

        i = 0
        for (cmd, coords, kwargs) in dwg.reproduce():
            # 1 color for LINE, 2 colors for the other 3 features
            if i < 4:
                """ 
                    the last TEXT in the self.test_features actually creates 2 entries
                """
                orig_cmd, *orig_clrs = self.test_features[i]

            self.assertEqual(cmd, orig_cmd)

            # OVAL, RECTANGLE, LINE
            if len(coords) == 4:
                self.assertListEqual(coords,
                                     [self.test_ev1.x, self.test_ev1.y, self.test_ev2.x, self.test_ev2.y])

                if cmd == LINE:
                    self.assertDictEqual(kwargs,
                                         {'fill': orig_clrs[0], 'width': 10})
                else:
                    self.assertDictEqual(kwargs,
                                         {'fill': orig_clrs[0], 'outline': orig_clrs[1], 'width': 10})

            # TEXT
            else:
                self.assertIn(coords,
                              ([self.test_ev1.x, self.test_ev1.y], [self.test_ev2.x, self.test_ev2.y]))
                self.assertEqual(kwargs['text'], "testi teksti")

            i += 1

    def test_2_user_cannot_see_others_dwgs(self):
        # this is a completely new user who has no drawings
        self.backend.login_register("user2", "user2")

        # user1 has 1 dwg in the DB at this point, but user2 shall not see it
        self.assertEqual(len(self.backend.get_user_dwgs()), 0)


# funny, this will not cleanUp if a test fails...
unittest.addModuleCleanup(lambda: os.unlink(TEST_DB))
