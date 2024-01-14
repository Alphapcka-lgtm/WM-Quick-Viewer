import pywmapi
from pywmapi.common.enums import Language
from pywmapi.auth.models import UserShort
from pywmapi.orders.models import OrderType
from datetime import datetime
import statistics


def get_items_dict(language: Language = Language.en):
    items_short = pywmapi.items.list_items(language)
    # XXX: Add liches and sisters stuff?
    items_dict = {item.item_name: item for item in items_short}
    return items_dict

def request_item_statistic_48h(url_name: str):
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

def request_item_orders(url_name: str):
    orders = pywmapi.orders.get_orders(url_name)
    orders = list(filter(lambda order: order.order_type == OrderType.sell and order.user.status == UserShort.Status.ingame, orders))
    orders = list(map(lambda order: order.platinum / order.quantity, orders))
    return orders

def item_price_from_statistics_or_order(url_name: str, date_median_price: dict[datetime, float]):
    """Berechned den Preis des Items von der übergeben Statistik oder requestet alle Orders für das Item, sollte es keine Statistiken geben."""
    if not date_median_price:
        orders = request_item_orders(url_name)
        return round(statistics.median(orders))
    
    return round(statistics.median(date_median_price.values()))
