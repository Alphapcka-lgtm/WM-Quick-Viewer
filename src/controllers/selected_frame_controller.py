from views.selected_frame import SelectedView, SelectedFrameTV
from views.item_view import ItemView
from models.warframe_market_model import WarframeMarketData
from models.market_item import MarketItem
from utils.observable_dict import ObservableDict
from controllers.item_view_controller import ItemViewController
from controllers.plot_frame_controller import PlotFrameController

from pywmapi.statistics.models import Statistic
from pywmapi.orders.models import OrderRow, OrderType, UserShort

import tkinter as tk

from typing import Literal
import re
import requests
from io import BytesIO
from PIL import Image, ImageTk
import statistics

class SelectedViewController:
    def __init__(self, view: SelectedView, model: WarframeMarketData) -> None:
        self.frame = view
        self.model = model
        self.model.selected_items.add_listener(self._on_item_selected)

        self._selected_views: dict[str, tuple[ItemView, ItemViewController]] = {}

        self._pf_ctrl: PlotFrameController = None
    
    @property
    def plot_frame_controller(self):
        return self._pf_ctrl
    
    @plot_frame_controller.setter
    def plot_frame_controller(self, ctlr: PlotFrameController):
        self._pf_ctrl = ctlr

    def _on_item_selected(self, mode: str, item_id: str, item: MarketItem):
        if mode == ObservableDict.ITEM_ADDED:
            interior = self.frame.items_frame.interior
            item_view = ItemView(interior)
            item_view.pack(side='bottom')


            iv_ctrl = ItemViewController(item_view, self.model, item)
            iv_ctrl.plot_frame_controller = self.plot_frame_controller
            
            self._selected_views[item_id] = (item_view, iv_ctrl)
            # interior.pack()
            # tk.Label(interior, text='is was just added!').pack()
        else:
            item_view, item_view_ctrl = self._selected_views[item_id]
            item_view.destroy()
            item_view_ctrl.rm_lang_listener()
            
            del item_view
            del item_view_ctrl

class SelectedFrameTVController:
    def __init__(self, view: SelectedFrameTV, model: WarframeMarketData) -> None:
        self.frame = view
        self.model = model
        self.model.selected_items.add_listener(self._on_selected_changed)

        self._pf_ctrl: PlotFrameController = None
        self._item_thumbs: dict[str, tuple[tk.PhotoImage, MarketItem]] = {}

        self._full_price = int(0)

        self._bind()
    
    @property
    def plot_frame_controller(self):
        return self._pf_ctrl
    
    @plot_frame_controller.setter
    def plot_frame_controller(self, ctlr: PlotFrameController):
        self._pf_ctrl = ctlr
    
    def _bind(self):
        self.frame.tv_selected_items.bind('<<TreeviewSelect>>', self._on_tv_item_selected)
        self.frame.btn_remove.config(command=self._rm_tv_item)
    
    def _on_selected_changed(self, action: str, item_id: str, item: MarketItem):
        if action is ObservableDict.ITEM_DEL:
            price_pq_str = self.frame.tv_selected_items.item(item_id, option='values')[2]
            price_pq = int(re.findall(r'\d+', price_pq_str)[0])
            self.frame.tv_selected_items.delete(item_id)
            del self._item_thumbs[item_id]
            self._update_full_price(action='sub', price_pq=price_pq)
            return
        
        img = self._create_item_tumb(item.thumb)
        price_po, price_pq = self._calculate_price(item)
        data = (item.quantity, f"{price_po} Platin", f"{price_pq} Platin")
        self.frame.tv_selected_items.insert(parent='', iid=item_id, index='end', image=img, text=item.get_lang_name(self.model.current_lang), values=data)
        self._item_thumbs[item_id] = (img, item)
        self._update_full_price(action='add', price_pq=price_pq)

    def _update_full_price(self, action: Literal["add", "sub"], price_pq: int):
        if action not in ("add", "sub"):
            raise KeyError(f'Unknown action: {action}')

        if action == "add":
            self._full_price += price_pq
        else:
            self._full_price -= price_pq
        self.frame.lbl_complete_price.config(text=f'Full price: {self._full_price}')

    def _create_item_tumb(self, thumb: str):
        thumb_url = 'https://warframe.market/static/assets/' + thumb
        response = requests.get(thumb_url)
        pil_img = Image.open(BytesIO(response.content))
        pil_img = pil_img.resize((round(pil_img.width / 3), round(pil_img.height / 3)))
        if pil_img.height > 30:
            pil_img = pil_img.resize((pil_img.width, 30))
        tk_img = ImageTk.PhotoImage(pil_img)
        return tk_img
    
    def _calculate_price(self, item: MarketItem):
        stats = item.statistics
        if stats.closed_48h == None or len(stats.closed_48h) == 0:
            return self._price_from_orders(item, item.orders)
        
        return self._price_from_stats(item, stats)
    
    def _price_from_stats(self, item: MarketItem, stats: Statistic):
        prices = list(map(lambda stat: stat.closed_price / stat.volume, stats.closed_48h))
        price_po = round(statistics.median(prices))
        price_pq = price_po * item.quantity
        return price_po, price_pq

    def _price_from_orders(self, item: MarketItem, orders: list[OrderRow]):
        orders_filtered = list(filter(lambda order: order.order_type == OrderType.sell and order.user.status == UserShort.Status.ingame, orders))
        prices = list(map(lambda order: order.platinum / order.quantity , orders_filtered))
        price_po = round(statistics.median(prices))
        price_pq = price_po * item.quantity
        return price_po, price_pq
    
    def _on_tv_item_selected(self, event):
        selection = self.frame.tv_selected_items.focus()
        if selection:
            self.frame.btn_remove.config(state='normal')
            self.plot_frame_controller.plot_item(self.model.get_item(selection))
            return
        
        self.frame.btn_remove.config(state='disabled')

    def _rm_tv_item(self):
        item_id = self.frame.tv_selected_items.focus()
        if not item_id:
            return
        
        self.model.rmv_selected(item_id)
