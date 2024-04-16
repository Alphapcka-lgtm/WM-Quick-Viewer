from models import *
from views.primes_ducats import PrimesDuctasWindow
import requests
from io import BytesIO
from PIL import Image, ImageTk
from models import api_requester
from tkinter import PhotoImage

class PrimesDuctasWindowController:
    def __init__(self, data: WarframeMarketData, view: PrimesDuctasWindow) -> None:
        self._wm_data = data
        self._view = view
        self._pr_data = PrimesRelicData(self._wm_data)
        self._ducats_plat_values = self._primes_ducats_values()
        self._item_thumbs: dict[str, tuple[PhotoImage, tuple[PrimeItem, MarketItem]]] = {}
        for prime, marketItem in self._ducats_plat_values:
            img = self._create_item_tumb(marketItem.thumb)
            price_po = marketItem.calculate_price()[0]
            ducats = prime.total_dacats_value()
            data = (f"{price_po} Platin", f"{ducats} Ducats", f"{ducats/price_po} d/p")
            self._view.tv_items.insert('', iid=marketItem.item_id, index='end', image=img, text=marketItem.get_lang_name(Language.en), values=data)
            self._item_thumbs[marketItem.item_id] = (img, marketItem)
    
    def _primes_ducats_values(self):
        primes_marketItems = self._pr_data.primes_with_market_item()
        print('requesting price data')
        for _, market_item in primes_marketItems:
            if market_item.statistics is None:
                market_item.statistics = api_requester.request_item_statistics(market_item.url_name)
            if market_item.orders is None:
                market_item.orders = api_requester.request_item_orders(market_item.url_name)
        print('done requesting')
        primes_marketItems.sort(key=lambda x: x[0].total_dacats_value() / x[1].calculate_price()[0])
        return primes_marketItems

    def _create_item_tumb(self, thumb: str):
        thumb_url = 'https://warframe.market/static/assets/' + thumb
        response = requests.get(thumb_url)
        pil_img = Image.open(BytesIO(response.content))
        pil_img = pil_img.resize((round(pil_img.width / 3), round(pil_img.height / 3)))
        if pil_img.height > 30:
            pil_img = pil_img.resize((pil_img.width, 30))
        tk_img = ImageTk.PhotoImage(pil_img)
        return tk_img
