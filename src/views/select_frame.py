import tkinter as tk
from tkinter import Misc
from tkinter import ttk
from pywmapi.common.enums import Language
from utils.string_list_var import ListStringVar

class SelectFrame(ttk.Frame):
    def __init__(self, master: Misc):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)

        ttk.Label(self, text='Items').grid(column=0, row=0, padx=10, sticky='NW')

        items_frame = ttk.Frame(self)
        self.items_search_entry = ttk.Entry(items_frame, validate='key')
        y_scroll = ttk.Scrollbar(items_frame, orient=tk.VERTICAL)
        self.items_var = ListStringVar()
        self.items_lb = tk.Listbox(items_frame, activestyle='dotbox', yscrollcommand=y_scroll.set, listvariable=self.items_var)
        y_scroll['command'] = self.items_lb.yview
        y_scroll.config(command=self.items_lb.yview)
        # y_scroll.grid(column=1, row=2, padx=10, sticky=tk.N + tk.S, rowspan=3)
        # self.items_lb.grid(column=0, row=2, padx=10, sticky='WE', rowspan=3)
        self.items_search_entry.pack(side=tk.TOP, fill=tk.X)
        self.items_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.LEFT, fill=tk.Y)
        items_frame.grid(column=0, row=1, sticky='NSWE', padx=10, rowspan=3)

        ttk.Label(self, text='Quantity:').grid(column=1, row=0, padx=10, sticky='NW')

        self.quantity_entry = tk.Entry(self, validate='key', width=5)
        self.quantity_entry.insert(0, '1')
        self.quantity_entry.grid(column=1, row=1, padx=10, sticky='NW')
        
        ttk.Label(self, text='Multiplier:').grid(column=2, row=0, padx=10, sticky='NW')

        self.entry_tv = tk.DoubleVar()
        self.entry_tv.set(0.60)
        self.multiplier_entry = ttk.Entry(self, validate='key', width=5, textvariable=self.entry_tv)
        self.multiplier_entry.grid(column=2, row=1, padx=10, sticky='NW')

        self.btn_add = ttk.Button(self, text='>> add >>', state='disabled')
        self.btn_add.grid(column=1, row=3, padx=10, pady=10, sticky='WE', columnspan=2)
