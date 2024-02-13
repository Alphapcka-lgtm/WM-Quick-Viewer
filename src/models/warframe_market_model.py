import pywmapi
from pywmapi.common.enums import Language
from pywmapi.auth.models import UserShort
from pywmapi.orders.models import OrderType
from pywmapi.items.models import ItemShort
from models.market_item import MarketItem
from datetime import datetime
from utils.observable_dict import ObservableDict
import statistics

class WarframeMarketData:

    def __init__(self, langs: set[Language]) -> None:
        self.langs = langs
        self.items_dict = self._get_items_lang_dict(self.langs)

        self.selected_items: ObservableDict[str, MarketItem] = ObservableDict()
    
    def item_names(self, lang: Language) -> list[str]:
        return [item.get_lang_name(lang) for item in self.items_dict.values()]
    
    def item_names_excluded(self, lang: str) -> list[str]:
        full_names = self.item_names(lang)
        if len(self.selected_items) == 0:
            return full_names
        
        return list(filter(lambda item: item not in self.selected_items[lang].keys(), full_names))
    
    def get_item(self, item_id: str):
        return self.items_dict[item_id]
    
    def get_item_statistics(self, item_url_name: str):
        return self._request_item_statistic_48h(item_url_name)
    
    def get_item_orders(self, item_url_name: ItemShort):
        return self._request_item_orders(item_url_name)
    
    def calculate_price(self, prices: list[int]) -> int:
        return round(statistics.median(prices))
    
    def name_to_id(self, item_name: str, lang: Language) -> str | None:
        for item in self.items_dict.values():
            if item.get_lang_name(lang) == item_name:
                return item.item_id
        return None
    
    def add_selected(self, item_id: str):
        item = self.items_dict[item_id]
        self.selected_items[item_id] = item
    
    def rmv_selected(self, item_id: str):
        self.items_dict.pop(item_id)
    
    def _get_items_lang_dict(self, langs: set[Language]):
        langs_iter = iter(langs)
        first_lang = next(langs_iter)
        items = pywmapi.items.list_items(first_lang)

        items_dict: dict[str, MarketItem] = {}
        for item in items:
            mi = MarketItem(item)
            mi.set_lang_name(first_lang, item.item_name)
            items_dict[item.id] = mi
        
        for lang in langs_iter:
            items = pywmapi.items.list_items(lang)
            for short_item in items:
                if short_item.id not in items_dict:
                    raise KeyError('TODO: item id not in items_dict')
                items_dict[short_item.id].set_lang_name(lang, short_item.item_name)
        
        return items_dict

    def _request_item_statistic_48h(self, url_name: str):
        stats = pywmapi.statistics.get_statistic(url_name)
        if len(stats.closed_48h) == 0:
            return None
        date_prices: dict[datetime, list[float]] = {}
        for stat in stats.closed_48h:
            if stat.datetime in date_prices.keys():
                date_prices[stat.datetime].append(stat.closed_price / stat.volume)
            else:
                date_prices[stat.datetime] = [stat.closed_price / stat.volume]

        date_median_price = {date: round(statistics.median(prices)) for date, prices in date_prices.items()}

        return date_median_price

    def _request_item_orders(self, url_name: str):
        orders = pywmapi.orders.get_orders(url_name)
        orders = list(filter(lambda order: order.order_type == OrderType.sell and order.user.status == UserShort.Status.ingame, orders))
        orders = list(map(lambda order: order.platinum / order.quantity, orders))
        return orders

    def item_price_from_statistics_or_order(self, url_name: str, date_median_price: dict[datetime, float]):
        """Berechned den Preis des Items von der übergeben Statistik oder requestet alle Orders für das Item, sollte es keine Statistiken geben."""
        if not date_median_price:
            orders = self._request_item_orders(url_name)
            return round(statistics.median(orders))

        return round(statistics.median(date_median_price.values()))
