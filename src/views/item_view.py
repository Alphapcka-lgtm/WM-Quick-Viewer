import tkinter as tk
from tkinter import Misc
from models.market_item import MarketItem
import requests
import io
from PIL import Image, ImageTk
from pywmapi.common.enums import Language

class ItemView(tk.Frame):
    def __init__(self, master: Misc, item: MarketItem) -> None:
        super().__init__(master, highlightbackground="darkgrey", highlightthickness=2, borderwidth=0)

        # self.pack(fill=tk.BOTH, expand=1)

        thumb = item.thumb
        url = 'https://warframe.market/static/assets/' + thumb
        response = requests.get(url)
        im = Image.open(io.BytesIO(response.content))
        # im = im.resize((60, 60))
        # im = im.reduce(2)
        im = im.resize((int(im.width / 1.5), int(im.height / 1.5)))
        img = ImageTk.PhotoImage(im)
        self.item_thumb = tk.Label(self, image=img)
        self.item_thumb.image = img
        self.item_thumb.place(x=0, y=5, anchor='nw')

        self.item_name = tk.Label(self, text=item.get_lang_name(Language.en), font='Helvetica 10 bold')
        self.item_name.place(x=90, y=5, anchor='nw')

        self.item_price_single = tk.Label(self, text='Item price per one: <Item price single>')
        self.item_price_single.place(x=90, y=25, anchor='nw')

        self.item_price_quantity = tk.Label(self, text='Item price quantity: <Item price quantity>')
        self.item_price_quantity.place(x=90, y=45, anchor='nw')
        self.config(width=350, height=80)
        self.pack(fill=tk.BOTH, expand=1)
