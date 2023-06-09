import json


class EmptyStackError(Exception):
    """Raised when there's no more features to un-/redo"""


class Drawing:
    """A log for reproducing each change in exact order as happened to the Canvas
    """

    def __init__(self, name: str, width=800, height=600, dwg_id: int = None, content: list = None):
        """(Re-)Creates a Drawing

        Args:
            name (str): title of the drawing
            width (int, optional): width of dwg. Defaults to 800.
            height (int, optional): height of dwg. Defaults to 600.
            dwg_id (int, optional): id of dwg. Defaults to None.
            content (list, optional): content of dwg. Defaults to None.
        """
        self.name = name
        self.id = dwg_id
        self.width = width
        self.height = height
        self._content = content if content else []
        self._undo_stack = []

    def add(self, cmd, *args, **kwargs):
        """Buffers used commands in a reproducible way
        """
        self._content.append((cmd, args, kwargs))

    def reproduce(self):
        """Used upon opening a dwg

        Yields:
            feature (tuple): in the form of (command, coords, kwargs)
        """
        for feature in self._content:
            yield feature

    def stringify(self):
        """Stringifies the content of the drawing
        """
        return json.dumps(self._content)

    def undo(self):
        """Moves the last feature to the undo stack
        """
        length = len(self._content)
        if length > 0:
            self._undo_stack.append(self._content.pop())
            return length-1 > 0

        raise EmptyStackError("no content left")

    def clear_undo_stack(self):
        """Forgets the rest of undone features
        """
        if len(self._undo_stack) > 0:
            self._undo_stack.clear()

    def redo(self):
        """Return the last undone feature to the log
        """
        length = len(self._undo_stack)
        if length > 0:
            feature = self._undo_stack.pop()
            self._content.append(feature)
            return feature, length-1 > 0

        raise EmptyStackError("nothing on the undo stack")
