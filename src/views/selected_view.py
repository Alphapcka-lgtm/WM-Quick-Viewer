import tkinter as tk
from tkinter import Misc
from views.vertical_scrolled_frame import VerticalScrolledFrame

class SelectedView(tk.Frame):
    def __init__(self, master: Misc) -> None:
        super().__init__(master)

        # tk.Label(self, text='').grid(column=0, row=0)
        # tk.Label(self, text='').grid(column=0, row=1)

        self.items_frame = VerticalScrolledFrame(self)
        self.items_frame.grid(column=0, row=0, sticky='NESW', padx=10, rowspan=3)
