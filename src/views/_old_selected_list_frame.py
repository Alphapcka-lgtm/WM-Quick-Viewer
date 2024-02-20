import tkinter as tk
from tkinter import Misc
from utils.string_list_var import ListStringVar


class SelectedListFrame(tk.Frame):
    def __init__(self, master: Misc) -> None:
        super().__init__(master)

        tk.Label(self, text='').grid(column=0, row=0)
        tk.Label(self, text='').grid(column=0, row=1)

        items_frame = tk.Frame(self)
        self.items_search_entry = tk.Entry(items_frame)
        y_scroll = tk.Scrollbar(items_frame, orient=tk.VERTICAL)
        self.items_var = ListStringVar()
        self.items_var.set([i for i in range(50)])
        self.items_lb = tk.Listbox(items_frame, activestyle='dotbox', yscrollcommand=y_scroll.set, listvariable=self.items_var)
        y_scroll['command'] = self.items_lb.yview
        y_scroll.config(command=self.items_lb.yview)
        # y_scroll.grid(column=1, row=2, padx=10, sticky=tk.N + tk.S, rowspan=3)
        # self.items_lb.grid(column=0, row=2, padx=10, sticky='WE', rowspan=3)
        self.items_search_entry.grid(column=0, row=0, columnspan=2, sticky='EW')
        self.items_lb.grid(column=0, row=1, sticky='NS')
        y_scroll.grid(column=1, row=1, sticky='NS')
        self.button_bar = SelectedButtonBar(items_frame)
        self.button_bar.grid(column=0, row=2, columnspan=2, sticky='EW')
        items_frame.grid(column=0, row=2, sticky='NESW', padx=10, rowspan=3)
    
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
        self.remove_button.pack(side=tk.LEFT, fill='x')
        self.prices_button.pack(side=tk.LEFT, fill='x')

    def activate_remove_btn(self):
        self.remove_button.config(state='normal')

    # def deactive_remove_btn(self):
    #     self.remove_button.config(state='disabled')

    def _remove_btn_cmd(self):
        self.selected.remove_selected()
