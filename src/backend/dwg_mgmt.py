import json
from collections import deque
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
        self._coords = deque()
        self._canvas = None
        self._canv_hist = None
        self._undo_btn_setter = None

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

    def set_canvas(self, canvas, undo_btn_setter: callable):
        """Assigns the current canvas to dwg_mgr, also re-draws the current drawing
        """
        self._canvas = canvas
        self._canv_hist = []
        self._undo_btn_setter = undo_btn_setter
        for (feature, coords, kwargs) in self._curr_dwg.reproduce():
            self._draw(feature, *coords, logging=False, **kwargs)

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

    def _draw(self, cmd: int, *args, logging: bool = True, **kwargs):
        """Creates features on the canvas + stores recipie in drawing's log

        Args:
            cmd (int): can be one of RECTANGLE, OVAL, LINE, TEXT
            logging (bool, optional): whether the feature should be added to the persistent
                                      storage or not. Defaults to True.
        """
        if cmd == RECTANGLE:
            self._canv_hist.append(
                self._canvas.create_rectangle(*args, **kwargs))

        elif cmd == OVAL:
            self._canv_hist.append(
                self._canvas.create_oval(*args, **kwargs))

        elif cmd == LINE:
            self._canv_hist.append(
                self._canvas.create_line(*args, **kwargs))

        elif cmd == TEXT:
            self._canv_hist.append(
                self._canvas.create_text(*args, **kwargs))

        if logging:
            self._curr_dwg.add(cmd, *args, **kwargs)
            self._undo_btn_setter()
            self._curr_dwg.clear_undo_stack()

    def b1_dn(self, event):
        """Left mouse button pressed
        """

    def b1_up(self, event, test_helper: str = None):
        """Left mouse button released

        Args:
            event (tkinter event): X and Y coords are used
            test_helper (str, optional): used during tests only. Defaults to None.
        """
        self._coords.append(event.x)
        self._coords.append(event.y)

        # keeping track of only 2(x,y) coords
        while len(self._coords) > 4:
            self._coords.popleft()

        if self._curr_cmd == TEXT:

            self._draw(self._curr_cmd, self._coords[-2], self._coords[-1],
                       text=test_helper if test_helper else self._text_prompter(),
                       fill=self._curr_fill)

        else:
            self._clicks += 1

            if self._clicks % 2 == 0:

                if self._curr_cmd == LINE:
                    self._draw(self._curr_cmd, *self._coords,
                               fill=self._curr_fill, width=10)
                else:
                    self._draw(self._curr_cmd, *self._coords,
                               outline=self._curr_border, fill=self._curr_fill, width=10)

    # jatkokehari?
    def b1_mv(self, event):
        """Dragged while left mouse button is pressed
        """

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
            self._draw(cmd, *coords, logging=False, **kwargs)
            return state

        except EmptyStackError:
            return False


dwg_mgr = DrawingManager()
