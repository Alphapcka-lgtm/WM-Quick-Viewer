import tkinter as tk
from tkinter import ttk

class PrimesDuctasWindow(tk.Toplevel):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.title('Primes Ducats')
        self.geometry("200x200")

        ttk.Label(self, text='Hello new window!').pack()
        self._tv_items = ttk.Treeview(self, columns=('price_mean', 'ducats', 'ducates_per_plat'))
        self._tv_items.heading('#0', text='Item Name')
        self._tv_items.heading('price_mean', text='Meadian Price')
        self._tv_items.heading('ducats', text='Ducats')
        self._tv_items.heading('ducats_per_plat', text='ducats per platinum')
