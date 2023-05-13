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
    # pylint: disable=bare-except
    def setUp(self):
        user_mgr.login_register("user", "user", lambda: "user")
        try:
            self.dwg = dwg_mgr.get_user_dwgs(user_mgr.get_curr_user().id)[0]
        except:
            self.dwg = Drawing(TITLE, WIDTH, HEIGHT)
        finally:
            dwg_mgr.set_curr_dwg(self.dwg)
            dwg_mgr.set_canvas(DummyCanvas(), dummy_callback)
            dwg_mgr.set_text_prompter(lambda: None)


    def test_0_save_empty_dwg(self):
        dwg_mgr.save_curr_dwg()


    def test_1_user_cannot_see_others_dwgs(self):
        # re-logging as a completely new user who has no drawings
        user_mgr.login_register("user2", "user2", lambda: "user2")

        # user1 has 1 dwg in the DB at this point, but user2 shall not see it
        self.assertEqual(len(dwg_mgr.get_user_dwgs(
            user_mgr.get_curr_user().name)), 0)


    def test_2_undo_redo_raise_on_empty_stack(self):
        # Drawing shall raise
        self.assertRaises(EmptyStackError, self.dwg.undo)

        # dwg_mgr turns that to boolean False
        self.assertFalse(dwg_mgr.undo())

        # Drawing shall raise
        self.assertRaises(EmptyStackError, self.dwg.redo)

        # dwg_mgr turns that to boolean False
        self.assertFalse(dwg_mgr.redo())


    def test_3_add_features_to_dwg(self):
        self.assertEqual(self.dwg, dwg_mgr.get_curr_dwg())

        # adding 4 features
        for (cmd, fill, border) in FEATURES:
            dwg_mgr.set_cmd(cmd)
            dwg_mgr.set_fill(fill)
            dwg_mgr.set_border(border)

            if cmd == TEXT:
                dwg_mgr.b1_up(EVENTS[4], "testi teksti")
            else:
                # press button 1
                dwg_mgr.b1_dn(EVENTS[0])

                # drag the mouse
                dwg_mgr.b1_mv(EVENTS[1])
                dwg_mgr.b1_mv(EVENTS[2])
                dwg_mgr.b1_mv(EVENTS[3])

                # relaese button 1
                dwg_mgr.b1_up(EVENTS[4])

        dwg_mgr.save_curr_dwg()


    def test_4_dwg_stored_features(self):
        self.assertTupleEqual(
            (TITLE, WIDTH, HEIGHT),
            (self.dwg.name, self.dwg.width, self.dwg.height))

        for i, (cmd, coords, kwargs) in enumerate(self.dwg.reproduce()):
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


    def test_5_dwg_undo_redo_non_empty_stacks(self):
        for _ in range(len(FEATURES)-1):
            self.assertTrue(dwg_mgr.undo())

        # False on last feature
        self.assertFalse(dwg_mgr.undo())

        for _ in range(len(FEATURES)-1):
            self.assertTrue(dwg_mgr.redo())

        # False on last feature
        self.assertFalse(dwg_mgr.redo())


    def test_6_dwg_clear_undo_stack(self):
        dwg_mgr.undo()
        dwg_mgr.set_cmd(TEXT)

        # Drawing.clear_undo_stack() gets triggered here
        dwg_mgr.b1_up(EVENTS[4])
