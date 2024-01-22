import tkinter as tk
from tkinter import  Misc
import pywmapi


class SelectedListFrame(tk.Frame):

    def __init__(self, master: Misc) -> None:
        super().__init__(master)

        self.var = tk.StringVar()
        self.var.set([i for i in range(50)])
        # self.list_box = tk.Listbox(self, listvariable=self.var)
        self.list_box = tk.Listbox(self)
        item = pywmapi.items.get_item('stunning_speed')[0]
        val = TestVal(item.en.item_name, item.url_name)
        self.list_box.insert(0, val)
        self.list_box.pack(padx=10)
        self.list_box.bind('<<ListboxSelect>>', self._on_item_select)

    def _on_item_select(self, event: tk.Event):
        sel = self.list_box.curselection()
        val = self.list_box.get(sel[0])
        print(val)

class TestVal(tk.StringVar):
    def __init__(self, master: Misc | None = None, value: str | None = None, name: str | None = None) -> None:
        super().__init__(master, value, name)
    
    def set(self, display_value: str) -> None:
        return super().set(display_value)
