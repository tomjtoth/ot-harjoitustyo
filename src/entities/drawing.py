class Drawing:
    """
        A drawing or a template modifiable by users
        Basically a log for reproducing each change in order happened to the Canvas
    """

    def __init__(self, name: str, width=800, height=600, content = None):
        "creates a Drawing"

        self._name = name
        self._content = content

    def add_rect(self):
        "adds a rectangle"
        pass

    def add_oval(self):
        "adds an oval"
        pass

    def add_line(self):
        "adds a line"
        pass

    def add_freeline(self):
        "adds freeline"
        pass
    
    def add_polygon(self):
        "adds a polygon"
        pass
