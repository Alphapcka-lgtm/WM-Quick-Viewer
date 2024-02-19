import tkinter as tk
from tkinter import ttk

class LangSelectView(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)

        ttk.Label(self, text='Item lang:').pack(side='left', padx=10, anchor='w')
        self.lang_cmb = ttk.Combobox(self, state='readonly', textvariable=tk.StringVar())
        # self.lang_cmb.grid(column=1, row=0, padx=10, sticky='W')
        self.lang_cmb.pack(side='left', padx=10, anchor='w')
