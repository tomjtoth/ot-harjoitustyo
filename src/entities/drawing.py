class Drawing:
    "A drawing or a template modifiable by users"

    def __init__(self, name: str, width=800, height=600, content = None):
        "creates a Drawing"

        self._name = name
        self._content = content

    def add_rect(self):
        pass

    def add_oval(self):
        pass

    def add_line(self):
        pass

    def add_freeline(self):
        pass
    
    def add_polygon(self):
        pass
