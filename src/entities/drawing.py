import json

class Drawing:
    """
        A drawing or a template modifiable by users
        Basically a log for reproducing each change in exact order as happened to the Canvas
    """

    def __init__(self, name: str, width = 800, height = 600, id: int = None, content: list = None):
        "creates a Drawing, width and height will be adjustable later prolly"

        self.name = name
        self.id = id
        self.width = width
        self.height = height
        self._content = content if content else []

    def add(self, cmd, *args, **kwargs):
        "buffers used commands in a reproducible way, probably in JSON format in backend"

        self._content.append([cmd, args, kwargs])

    def reproduce(self):
        "this could probably be a simple getter..."

        for feature in self._content:
            yield feature
            
    def stringify(self):
        "this output is saved to backend"

        return json.dumps(self._content)

