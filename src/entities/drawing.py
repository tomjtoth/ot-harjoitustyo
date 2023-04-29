import json


class EmptyStackError(Exception):
    """Raised when there's no more features to un-/redo"""


class Drawing:
    """
        A drawing or a template modifiable by users
        Basically a log for reproducing each change in exact order as happened to the Canvas
    """

    def __init__(self, name: str, width=800, height=600, dwg_id: int = None, content: list = None):
        """creates a Drawing"""

        self.name = name
        self.id = dwg_id
        self.width = width
        self.height = height
        self._content = content if content else []
        self._undo_stack = []

    def add(self, cmd, *args, **kwargs):
        """buffers used commands in a reproducible way"""

        self._content.append((cmd, args, kwargs))

    def reproduce(self):
        """used when reproducing a drawing upon opening it"""

        for feature in self._content:
            yield feature

    def stringify(self):
        """stringifies the content of the drawing, used for saving to backend"""

        return json.dumps(self._content)

    def undo(self):
        """moves the last feature to the undo stack"""
        length = len(self._content)
        if length > 0:
            self._undo_stack.append(self._content.pop())
            return length-1 > 0

        raise EmptyStackError('no content left')

    def clear_undo_stack(self):
        """forgets the rest of undone features"""
        if len(self._undo_stack) > 0:
            self._undo_stack.clear()

    def redo(self):
        """If there's something on the undo stack, return it to the drawing"""
        length = len(self._undo_stack)
        if length > 0:
            feature = self._undo_stack.pop()
            self._content.append(feature)
            return feature, length-1 > 0

        raise EmptyStackError('nothing on the undo stack')
