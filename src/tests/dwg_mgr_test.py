import unittest
import os
from entities.drawing import Drawing, EmptyStackError

# TESTING must be set before importing either user_mgr or dwg_mgr
os.environ.setdefault("TESTING", "setting this here for Backend")

# pylint: disable=wrong-import-position
from backend.dwg_mgmt import dwg_mgr, RECTANGLE, OVAL, LINE, TEXT
from backend.user_mgmt import user_mgr

# needed because these tests build on top of each other, test order is strict
unittest.TestLoader.sortTestMethodsUsing = None

class DummyEvent:
    """mimicking user clicks to tkinter.Canvas
    """
    # pylint: disable=invalid-name
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def dummy_callback():
    """Backend._draw() spams the undo button into NORMAL state
    """

TITLE, WIDTH, HEIGHT = "4 features at 20,20,100,100", 640, 480
FEATURES = (
    (OVAL, "purple", "black"),
    (RECTANGLE, "green", "yellow"),
    (LINE, "blue", "gray"),
    (TEXT, "red", "white"))
EVENTS = [DummyEvent(x, x) for x in (20, 40, 60, 80, 100)]


class DummyCanvas:
    """
        Backend._draw(...) heavily integrates with tkinter.Canvas
        These methods are called during normal operation
        I only need to check on the logging capability of my Drawing
    """

    def create_rectangle(self, *_args, **_kwargs):
        return 1

    def create_oval(self, *_args, **_kwargs):
        return 1

    def create_line(self, *_args, **_kwargs):
        return 1

    def create_text(self, *_args, **_kwargs):
        return 1

    def delete(self, obj):
        pass

class TestDrawing(unittest.TestCase):
    def setUp(self):
        user_mgr.login_register("user", "user", lambda: "user")
        

    def test_0_save_new_dwg_complex(self):
        dwg = Drawing(TITLE, WIDTH, HEIGHT)
        dwg_mgr.set_curr_dwg(dwg)
        dwg_mgr.set_canvas(DummyCanvas(), dummy_callback)
        dwg_mgr.set_text_prompter(lambda: None)

        self.assertEqual(dwg, dwg_mgr.get_curr_dwg())

        # adding 4 features
        for (cmd, fill, border) in FEATURES:
            dwg_mgr.set_cmd(cmd)
            dwg_mgr.set_fill(fill)
            dwg_mgr.set_border(border)

            # emulate user clicks
            if cmd == TEXT:
                dwg_mgr.b1_up(EVENTS[4], "testi teksti")
            else:
                dwg_mgr.b1_dn(EVENTS[0])
                dwg_mgr.b1_mv(EVENTS[1])
                dwg_mgr.b1_mv(EVENTS[2])
                dwg_mgr.b1_mv(EVENTS[3])
                dwg_mgr.b1_up(EVENTS[4])

        dwg_mgr.save_curr_dwg()

    def test_1_dwg_content_intact(self):
        dwg = dwg_mgr.get_user_dwgs(user_mgr.get_curr_user().id)[0]

        self.assertTupleEqual(
            (TITLE, WIDTH, HEIGHT),
            (dwg.name, dwg.width, dwg.height))

        for i, (cmd, coords, kwargs) in enumerate(dwg.reproduce()):
            orig_cmd, *orig_clrs = FEATURES[i]
            self.assertEqual(cmd, orig_cmd)

            # OVAL, RECTANGLE, LINE
            if len(coords) == 4:
                self.assertListEqual(coords,
                                     [EVENTS[0].x, EVENTS[0].y,
                                      EVENTS[4].x, EVENTS[4].y])

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
                              ([EVENTS[0].x, EVENTS[0].y],
                               [EVENTS[4].x, EVENTS[4].y]))
                self.assertEqual(kwargs["text"], "testi teksti")

    def test_2_user_cannot_see_others_dwgs(self):
        # this is a completely new user who has no drawings
        user_mgr.login_register("user2", "user2", lambda: "user2")

        # user1 has 1 dwg in the DB at this point, but user2 shall not see it
        self.assertEqual(len(dwg_mgr.get_user_dwgs(
            user_mgr.get_curr_user().name)), 0)

    def test_3_dwg_undo_redo_works(self):
        dwg = dwg_mgr.get_user_dwgs(user_mgr.get_curr_user().id)[0]
        dwg_mgr.set_curr_dwg(dwg)
        dwg_mgr.set_canvas(DummyCanvas(), dummy_callback)

        for _ in range(len(FEATURES)-1):
            self.assertTrue(dwg_mgr.undo())

        # 1 on stack, remains 0 -> False
        self.assertFalse(dwg_mgr.undo())
        # 0 on stack -> False
        self.assertFalse(dwg_mgr.undo())
        self.assertRaises(EmptyStackError, dwg.undo)

        for _ in range(len(FEATURES)-1):
            self.assertTrue(dwg_mgr.redo())

        # 1 on stack, remains 0 -> False
        self.assertFalse(dwg_mgr.redo())
        # 0 on stack -> False
        self.assertFalse(dwg_mgr.redo())
        self.assertRaises(EmptyStackError, dwg.redo)

        # saving already existing dwg here
        dwg_mgr.save_curr_dwg()

        # Drawing.clear_undo_stack() simulated
        dwg_mgr.undo()
        dwg_mgr.set_cmd(TEXT)
        #dwg_mgr.b1_dn(EVENTS[0])
        dwg_mgr.b1_up(EVENTS[4])
