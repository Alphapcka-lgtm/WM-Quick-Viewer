import pywmapi
from pywmapi.common.enums import Language
from pywmapi.auth.models import UserShort
from pywmapi.orders.models import OrderType
from datetime import datetime
import statistics


def get_items_dict(language: Language = Language.en):
    items_short = pywmapi.items.list_items(language)
    items_short[0]
    items_dict = {item.item_name: item for item in items_short}
    return items_dict

def get_item_statistic_48h(url_name: str):
    stats = pywmapi.statistics.get_statistic(url_name)
    if len(stats.closed_48h) == 0:
        return None
    date_prices: dict[datetime, list[float]] = {}
    for stat in stats.closed_48h:
        if stat.datetime in date_prices.keys():
            date_prices[stat.datetime].append(stat.closed_price / stat.volume)
        else:
            date_prices[stat.datetime] = [stat.closed_price / stat.volume]
    
    date_median_price = {date: statistics.median(prices) for date, prices in date_prices.items()}

    return date_prices, date_median_price

def get_item_price(url_name: str):
    stats_tuple = get_item_statistic_48h(url_name)
    if stats_tuple == None:
        orders = pywmapi.orders.get_orders(url_name)
        orders = list(filter(lambda order: order.user.status == UserShort.Status.ingame and order.order_type == OrderType.sell, orders))
        prices_per_one = list(map(lambda order: order.platinum / order.quantity, orders))
        return round(statistics.median(prices_per_one))
    
    date_median_price = stats_tuple[1]
    return round(statistics.median(date_median_price.values()))
