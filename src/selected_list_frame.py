import tkinter as tk
from tkinter import Misc
from controller import Controller
import pywmapi


class SelectedListFrame(tk.Frame):

    def __init__(self, master: Misc, controller: Controller) -> None:
        super().__init__(master)

        self.controller = controller

        self.var = tk.StringVar()
        self.var.set([i for i in range(50)])
        # self.list_box = tk.Listbox(self, listvariable=self.var)
        self.list_box = tk.Listbox(self, listvariable=self.var)
        # item = pywmapi.items.get_item('stunning_speed')[0]
        self.list_box.pack(padx=10)
        self.list_box.bind('<<ListboxSelect>>', self._on_item_select)
        self.button_bar = SelectedButtonBar(self)
    
    def remove_selected(self):
        selection_index: int = self.list_box.curselection()[0]
        self.list_box.delete(selection_index, selection_index)
    
    def get_selected(self) -> list[str]:
        return self.list_box.get(0, tk.END)

    def _on_item_select(self, event: tk.Event):
        self.button_bar.activate_remove_btn()
        sel = self.list_box.curselection()
        val = self.list_box.get(sel[0])
        print(val)

class SelectedButtonBar(tk.Frame):

    def __init__(self, master: SelectedListFrame) -> None:
        super().__init__(master)
        self.selected = master

        self.remove_button = tk.Button(self, text='X', fg='red', width=5, state='disabled', command=self._remove_btn_cmd)
        self.prices_button = tk.Button(self, text='Preis Berechnen')

    def activate_remove_btn(self):
        self.remove_button.config(state='normal')

    # def deactive_remove_btn(self):
    #     self.remove_button.config(state='disabled')

    def _remove_btn_cmd(self):
        self.selected.remove_selected()
