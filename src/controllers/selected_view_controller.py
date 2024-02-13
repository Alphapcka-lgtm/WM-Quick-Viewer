from views.selected_view import SelectedView
from views.item_view import ItemView
from models.warframe_market_model import WarframeMarketData
from models.market_item import MarketItem
from utils.observable_dict import ObservableDict

import tkinter as tk

class SelectedViewController:
    def __init__(self, view: SelectedView, model: WarframeMarketData) -> None:
        self.frame = view
        self.model = model
        self.model.selected_items.add_listener(self._on_item_selected)

    def _on_item_selected(self, mode: str, item_id: str, item: MarketItem):
        if mode == ObservableDict.ITEM_ADDED:
            interior = self.frame.items_frame.interior
            item_view = ItemView(interior, item)
            item_view.pack(side='bottom')
            # interior.pack()
            # tk.Label(interior, text='is was just added!').pack()
        else:
            print('Item was deleted!')
