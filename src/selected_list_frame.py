import tkinter as tk
from tkinter import  Misc


class SelectedListFrame(tk.Frame):
    def __init__(self, master: Misc) -> None:
        super().__init__(master)

        self.list_box = tk.Listbox(self)
        items = [i for i in range(50)]
        self.list_box.insert(0, *items)
        self.list_box.pack(padx=10)
