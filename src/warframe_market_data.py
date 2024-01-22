import pywmapi
from pywmapi.common.enums import Language
from pywmapi.auth.models import UserShort
from pywmapi.orders.models import OrderType
from pywmapi.items.models import ItemShort
from datetime import datetime
import statistics

class WarframeMarketData():

    def __init__(self, langs: list[Language]) -> None:
        self.items_langs_dict = self._get_items_lang_dict(langs)

    def get_langs(self) -> list[str]:
        return list(self.items_langs_dict.keys())
    
    def get_item_names(self, lang: str) -> list[str]:
        return list(self.items_langs_dict[lang].keys())
    
    def get_item(self, lang: str, name: str) -> ItemShort:
        return self.items_langs_dict[lang][name]
    
    def get_item_statistics(self, item: ItemShort):
        return self._request_item_statistic_48h(item.url_name)
    
    def get_item_orders(self, item: ItemShort):
        return self._request_item_orders(item.url_name)
    
    def calculate_price(prices: list[float]) -> int:
        return round(statistics.median(prices))
    
    def _get_items_lang_dict(self, langs: list[Language]):
        items_lang_dict = {lang.value: self._get_items_dict(lang) for lang in langs}
        return items_lang_dict

    def _get_items_dict(self, language: Language = Language.en):
        items_short = pywmapi.items.list_items(language)
        # XXX: Add liches and sisters stuff?
        items_dict = {item.item_name: item for item in items_short}
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
