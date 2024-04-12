import tkinter as tk
from tkinter import ttk

class PrimesDuctasWindow(tk.Toplevel):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.title('Primes Ducats')
        self.geometry("200x200")

        ttk.Label(self, text='Hello new window!').pack()
