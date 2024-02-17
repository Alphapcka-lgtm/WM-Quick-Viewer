import tkinter as tk
from tkinter import ttk
from tkinter import Misc
from models.market_item import MarketItem
import requests
import io
from PIL import Image, ImageTk
from pywmapi.common.enums import Language

class ItemView(tk.Frame):
    def __init__(self, master: Misc) -> None:
        super().__init__(master, highlightbackground="darkgrey", highlightthickness=2, borderwidth=0)

        self.item_thumb = tk.Label(self)
        # self.item_thumb.image = img
        self.item_thumb.place(x=0, y=5, anchor='nw')

        self.item_name = tk.Label(self, text='<item name>', font='Helvetica 10 bold')
        self.item_name.place(x=90, y=5, anchor='nw')

        self.item_price_single = tk.Label(self, text='Item price per one: <Item price single>')
        self.item_price_single.place(x=90, y=25, anchor='nw')

        self.item_price_quantity = tk.Label(self, text='Item price quantity: <Item price quantity>')
        self.item_price_quantity.place(x=90, y=45, anchor='nw')

        self.btn_graph = ttk.Button(self, text='Graph')
        self.btn_graph.place(x=0, y=63, anchor='w')
        self.config(width=350, height=80)
        self.pack(fill=tk.BOTH, expand=1)
