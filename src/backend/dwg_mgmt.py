import json
from entities.drawing import Drawing, EmptyStackError
from backend.database import db
from backend.user_mgmt import user_mgr

RECTANGLE = 0
OVAL = 1
LINE = 2
TEXT = 3


class DrawingManager:
    """Manages changes to tkinter.Canvas and the log (drawing)
    """

    def __init__(self):
        """Creates the manager
        """
        self._conn = db
        self._curr_dwg = None

        self._clicks = 0
        self._curr_cmd = RECTANGLE
        self._text_prompter = None
        self._curr_fill = "red"
        self._curr_border = "green"
        self._coords = None
        self._preview = None
        self._canvas = None
        self._canv_hist = None
        self._btn_state_setter = None

    def get_user_dwgs(self, user_id: int) -> list:
        """Retrieves all drawings of the user as a list
        """
        return [
            Drawing(name, width, height, dwg_id, json.loads(content))
            for name, width, height, dwg_id, content
            in self._conn.fetchall("""
            select name, width, height, id, content
            from drawings d
            where owner_id=?
            """, (user_id, ))
        ]

    def save_curr_dwg(self):
        """Dumps the log (drawing contents) as JSON to SQLite
        """
        # existing drawing
        if self._curr_dwg.id:
            self._conn.execute("""
            update drawings set content = ?
            where id = ?
            """, (self._curr_dwg.stringify(), self._curr_dwg.id))

        # new drawing
        else:
            self._conn.execute("""
            insert into drawings(
                owner_id,
                name,
                width,
                height,
                content
            ) values (?,?,?,?,?)
            """, (
                user_mgr.get_curr_user().id,
                self._curr_dwg.name,
                self._curr_dwg.width,
                self._curr_dwg.height,
                self._curr_dwg.stringify()
            ))

    def get_curr_dwg(self) -> Drawing:
        """Gets the current drawing
        """
        return self._curr_dwg

    def set_curr_dwg(self, dwg: Drawing):
        """Assigns the current drawing to dwg_mgr
        """
        self._curr_dwg = dwg

    def set_canvas(self, canvas, btn_state_setter: callable):
        """Assigns the current canvas to dwg_mgr, also re-draws the current drawing
        """
        self._canvas = canvas
        self._canv_hist = []
        self._btn_state_setter = btn_state_setter
        for (feature, coords, kwargs) in self._curr_dwg.reproduce():
            self._canv_hist.append(self._draw(feature, *coords, **kwargs))

    def set_cmd(self, cmd: int):
        """Sets the currently initiated command
        """
        self._curr_cmd = cmd

    def set_text_prompter(self, prompt: callable):
        """Makes backend able to call a pop-up window for querying the text
        """
        self._text_prompter = prompt

    def set_fill(self, color: str):
        """Sets the fill color for next features
        """
        self._curr_fill = color

    def set_border(self, color: str):
        """Sets the border color for next features
        """
        self._curr_border = color

    def _draw(self, cmd: int, *coords,  logging: bool = False, **kwargs):
        """Adds a feature to the canvas and optionally logs it

        Args:
            cmd (int): can be one ov RECTANGLE, OVAL, LINE, TEXT
            logging (bool, optional): used only on direct user interaction. Defaults to False.

        Returns:
            tkinter.feature: a pointer to the last added feature
        """

        if not kwargs:
            kwargs = {
                "fill": self._curr_fill,
                "width": 10}

            if cmd in (OVAL, RECTANGLE):
                kwargs["outline"] = self._curr_border

        if cmd == RECTANGLE:
            feature = self._canvas.create_rectangle(*coords, **kwargs)

        elif cmd == OVAL:
            feature = self._canvas.create_oval(*coords, **kwargs)

        elif cmd == LINE:
            feature = self._canvas.create_line(*coords, **kwargs)

        elif cmd == TEXT:
            feature = self._canvas.create_text(*coords, **kwargs)

        if logging:
            self._curr_dwg.add(cmd, *coords, **kwargs)
            self._btn_state_setter()
            self._curr_dwg.clear_undo_stack()

        return feature

    def b1_dn(self, event):
        """Initiates drawing feature's preview

        Args:
            event (tkinter.event): mouse x,y are taken from here
        """
        if self._curr_cmd != TEXT:
            self._coords = (event.x, event.y)

    def b1_mv(self, event):
        """Drawing a preview of the feature to-be-added

        Args:
            event (tkinter.Event): mouse x,y are taken from here
        """
        if self._preview:
            self._canvas.delete(self._preview)

        if self._curr_cmd != TEXT:
            self._preview = self._draw(
                self._curr_cmd, *self._coords, event.x, event.y)

    def b1_up(self, event, test_helper: str = None):
        """Adding feature at mouse pos

        Args:
            event (tkinter.event): mouse x,y are taken from here
            test_helper (str, optional): used only during tests. Defaults to None.
        """

        if self._curr_cmd == TEXT:

            self._canv_hist.append(self._draw(
                self._curr_cmd, event.x, event.y,
                logging=True,
                text=test_helper if test_helper else self._text_prompter(),
                fill=self._curr_fill))

        else:
            self._canv_hist.append(self._draw(
                self._curr_cmd, *self._coords, event.x, event.y, logging=True))

        self._coords = None

        if self._preview:
            self._canvas.delete(self._preview)
            self._preview = None

    def undo(self):
        """Moves 1 feature from the contents of the dwg to the undo stack

        Returns:
            bool: True if there's more feaure in the dwg
        """
        try:
            state = self._curr_dwg.undo()
            self._canvas.delete(
                self._canv_hist.pop())
            return state

        except EmptyStackError:
            return False

    def redo(self):
        """Moves 1 feature from the undo stack to the contents of the dwg

        Returns:
            bool: True if there's more on the undo stack, else False
        """
        try:
            (cmd, coords, kwargs), state = self._curr_dwg.redo()
            self._canv_hist.append(self._draw(
                cmd, *coords, logging=False, **kwargs))
            return state

        except EmptyStackError:
            return False


dwg_mgr = DrawingManager()
