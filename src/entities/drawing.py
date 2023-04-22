import json


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

    def add(self, cmd, *args, **kwargs):
        """buffers used commands in a reproducible way"""

        self._content.append((cmd, args, kwargs))

    def reproduce(self):
        """this could probably be a simple getter..."""

        for feature in self._content:
            yield feature

    def stringify(self):
        """stringifies the content of the drawing, used for saving to backend"""

        return json.dumps(self._content)
