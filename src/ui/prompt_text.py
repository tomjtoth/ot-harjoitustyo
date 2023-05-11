from tkinter import Toplevel, StringVar, Label, Entry, Button


class PromptText(Toplevel):
    """Simple pop-up to query 1 string from the user
    """

    def __init__(self, master, title: str, kwlabel: dict, kwentry: dict, kwbutton: dict):
        """Creates the pop-up

        Args:
            master (tkinter.Frame): owner of pop-up
            title (str): Title of pop-up
            kwlabel (dict): kwargs for the label
            kwentry (dict): kwargs for the entry
            kwbutton (dict): kwargs for the button
        """
        super().__init__(master)
        self.title(title)

        self.__retval = StringVar(self)
        Label(self, **kwlabel).grid(column=0, row=0)
        entry = Entry(self, **kwentry, textvariable=self.__retval)
        entry.bind("<Return>", lambda _ev: self.destroy())
        entry.grid(column=1, row=0)
        entry.focus_set()

        Button(self, **kwbutton, command=self.destroy
               ).grid(columnspan=2, row=3)

    def get(self) -> str:
        """Waits for user input and returns it
        """

        self.wait_window()
        return self.__retval.get()
