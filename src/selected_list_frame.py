import tkinter as tk
from tkinter import  Misc


class SelectedListFrame(tk.Frame):

    def __init__(self, master: Misc) -> None:
        super().__init__(master)

        self.var = tk.StringVar()
        self.var.set([i for i in range(50)])
        self.list_box = tk.Listbox(self, listvariable=self.var)
        self.list_box.pack(padx=10)
