from models import WarframeMarketData
from models import MarketItem
from views.item_view import ItemView
from controllers.plot_frame_controller import PlotFrameController

import requests
from io import BytesIO
from PIL import Image, ImageTk
import statistics

# pywampi imports
from pywmapi.common.enums import Language, OrderType
from pywmapi.statistics.models import Statistic
from pywmapi.orders.models import OrderRow, UserShort

class ItemViewController:
    def __init__(self, view: ItemView, data: WarframeMarketData, item: MarketItem) -> None:
        self.item = item
        self.data = data
        self.frame = view
        self._rm_lang_listener = self.data.add_lang_change_observer(self._on_lang_change)

        self.frame.btn_graph.config(command=self._display_graph)
        self.frame.remove_btn.config(command=self._rmv_item_from_selected)

        self._pf_controller: PlotFrameController = None

        self._fill_view()

    @property
    def plot_frame_controller(self):
        return self._pf_controller
    
    @plot_frame_controller.setter
    def plot_frame_controller(self, ctrl: PlotFrameController):
        self._pf_controller = ctrl
    
    def rm_lang_listener(self):
        self._rm_lang_listener()
    
    def _fill_view(self):
        self.frame.item_name.config(text=self.item.get_lang_name(self.data.current_lang))
        img = self._create_item_tumb(self.item.thumb)
        self.frame.item_thumb.config(image=img)
        self.frame.item_thumb.image = img
        price_po, price_pq = self._calculate_price()
        self.frame.item_price_single.config(text=f'Item price per one: {price_po} Plat')
        self.frame.item_price_quantity.config(text=f'Item price quantity: {price_pq} Plat')
    
    def _create_item_tumb(self, thumb: str):
        thumb_url = 'https://warframe.market/static/assets/' + thumb
        response = requests.get(thumb_url)
        pil_img = Image.open(BytesIO(response.content))
        pil_img = pil_img.resize((round(pil_img.width / 1.5), round(pil_img.height / 1.5)))
        tk_img = ImageTk.PhotoImage(pil_img)
        return tk_img
    
    def _calculate_price(self):
        stats = self.item.statistics
        if stats.closed_48h == None or len(stats.closed_48h) == 0:
            return self._price_from_orders(self.item.orders)
        
        return self._price_from_stats(stats)
    
    def _price_from_stats(self, stats: Statistic):
        prices = list(map(lambda stat: stat.closed_price / stat.volume, stats.closed_48h))
        price_po = round(statistics.median(prices))
        price_pq = price_po * self.item.quantity
        return price_po, price_pq

    def _price_from_orders(self, orders: list[OrderRow]):
        orders_filtered = list(filter(lambda order: order.order_type == OrderType.sell and order.user.status == UserShort.Status.ingame, orders))
        prices = list(map(lambda order: order.platinum / order.quantity , orders_filtered))
        price_po = round(statistics.median(prices))
        price_pq = price_po * self.item.quantity
        return price_po, price_pq

    def _on_lang_change(self, lang: Language):
        self.frame.item_name.config(text=self.item.get_lang_name(lang))
    
    def _display_graph(self):
        self.plot_frame_controller.plot_item(self.item)
    
    def _rmv_item_from_selected(self):
        self.data.selected_items.pop(self.item.item_id)
