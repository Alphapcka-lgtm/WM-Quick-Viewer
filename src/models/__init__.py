from pywmapi.items.models import ItemShort
from pywmapi.statistics.models import Statistic
from pywmapi.orders.models import OrderRow, UserShort
from pywmapi.common.enums import Language, OrderType

import models.api_requester as api_requester
from typing import Callable
from utils.observable_dict import ObservableDict
import statistics


class WarframeMarketData:

    def __init__(self, langs: set[Language]) -> None:
        self.langs = langs
        self.items_dict = self._get_items_lang_dict(self.langs)

        self._current_lang: Language = Language.en
        self._lang_change_observers: list[Callable[[Language], None]] = []
        self.selected_items: ObservableDict[str, MarketItem] = ObservableDict()
    
    @property
    def current_lang(self):
        return self._current_lang
    
    @current_lang.setter
    def current_lang(self, lang: Language):
        if self.current_lang.value == lang.value:
            return
        self._current_lang = lang
        for callback in self._lang_change_observers:
            callback(self._current_lang)
    
    def item_names(self, lang: Language) -> list[str]:
        return [item.get_lang_name(lang) for item in self.items_dict.values()]
    
    def item_names_excluded(self, lang: Language) -> list[str]:
        full_names = self.item_names(lang)
        if len(self.selected_items) == 0:
            return full_names
        
        selected_names = [item.get_lang_name(lang) for item in self.selected_items.values()]
        return list(filter(lambda item_name: item_name not in selected_names, full_names))
    
    def get_item(self, item_id: str):
        return self.items_dict[item_id]
    
    def name_to_id(self, item_name: str, lang: Language) -> str | None:
        for item in self.items_dict.values():
            if item.get_lang_name(lang) == item_name:
                return item.item_id
        return None
    
    def add_selected(self, item_id: str, quantity: int, modifier: float):
        item = self.items_dict[item_id]
        item.quantity = quantity
        item.modifier = modifier
        item.statistics = api_requester.request_item_statistics(item.url_name)
        item.orders = api_requester.request_item_orders(item.url_name)
        self.selected_items[item_id] = item
    
    def rmv_selected(self, item_id: str):
        del self.selected_items[item_id]
        
    def add_lang_change_observer(self, func: Callable[[Language], None]):
        self._lang_change_observers.append(func)
        return lambda: self._lang_change_observers.remove(func)
    
    def _get_items_lang_dict(self, langs: set[Language]):
        langs_iter = iter(langs)
        first_lang = next(langs_iter)
        items = api_requester.request_items(first_lang)

        items_dict: dict[str, MarketItem] = {}
        for item in items:
            mi = MarketItem(item)
            mi.set_lang_name(first_lang, item.item_name)
            items_dict[item.id] = mi
        
        for lang in langs_iter:
            items = api_requester.request_items(lang)
            for short_item in items:
                if short_item.id not in items_dict:
                    raise KeyError('TODO: item id not in items_dict')
                items_dict[short_item.id].set_lang_name(lang, short_item.item_name)
        
        return items_dict
    
class MarketItem:
    def __init__(self, item_short: ItemShort) -> None:
        self.item_id = item_short.id
        self.url_name = item_short.url_name
        self.thumb = item_short.thumb
        self.localized_item_names: ObservableDict[str, str] = ObservableDict()

        self.quantity: int = 1
        self.modifier: float = 1.0
        self._statistics: Statistic = None
        self._orders: list[OrderRow] = None

    @property
    def statistics(self):
        return self._statistics
    
    @statistics.setter
    def statistics(self, stats: Statistic):
        self._statistics = stats

    @property
    def orders(self):
        return self._orders
    
    @orders.setter
    def orders(self, orders: list[OrderRow]):
        self._orders = orders

    def calculate_price(self):
        """
        Calculates the price of the market item.
        Returns a tuple with the median price for this item as a single quantatiy and the median price for the full quantaty set by order.
        """
        if self.statistics == None and self.orders == None:
            raise AttributeError('Neither statistics nor orders available!')
        stats = self.statistics
        if stats.closed_48h == None or len(stats.closed_48h) == 0:
            return self._price_from_orders(self.orders)
        
        return self._price_from_stats(stats)
    
    def _price_from_stats(self, stats: Statistic):
        prices = list(map(lambda stat: stat.closed_price / stat.volume, stats.closed_48h))
        price_po = round(statistics.median(prices))
        price_pq = price_po * self.quantity
        return price_po, price_pq

    def _price_from_orders(self, orders: list[OrderRow]):
        orders_filtered = list(filter(lambda order: order.order_type == OrderType.sell and order.user.status == UserShort.Status.ingame, orders))
        prices = list(map(lambda order: order.platinum / order.quantity , orders_filtered))
        price_po = round(statistics.median(prices))
        price_pq = price_po * self.quantity
        return price_po, price_pq

    def get_lang_name(self, lang: Language):
        return self.localized_item_names.get(lang.value, None)

    def set_lang_name(self, lang: Language, name: str):
        self.localized_item_names[lang.value] = name
    
    def remove_lang_name(self, lang: Language):
        self.localized_item_names.__delitem__(lang.value)

class PrimesRelicData:

    def __init__(self, wm_data: WarframeMarketData) -> None:
        if not Language.en in wm_data.langs:
            raise Exception('Data does not contain Language EN!')
        
        self.wm_data = wm_data
        self.prime_data = self._get_primes_data()
        self.names_sets = list(filter(lambda name: 'set' in name.lower(), self.wm_data.item_names(Language.en)))

    def primes_with_market_item(self) -> list[tuple['PrimeItem', MarketItem]]:
        """Returns a list with pairs of PrimeItem and MarketItem"""
        ret = []
        wm_names = self.wm_data.item_names(Language.en)
        for prime_item in self.prime_data:
            for wm_name in wm_names:
                if prime_item.name.lower() in wm_name.lower():
                    item_id = self.wm_data.name_to_id(wm_name, Language.en)
                    if item_id == None:
                        raise NameError(f'item name {wm_name} not found with an id!')
                    ret.append((prime_item, self.wm_data.get_item(item_id)))

        # for set_name in self.names_sets:
        #     for index, prime_item in enumerate(self.prime_data):
        #         if prime_item.name in set_name:
        #             item_id = self.wm_data.name_to_id(set_name, Language.en)
        #             ret.append((prime_item, self.wm_data.get_item(item_id)))
        #             # remove the item from the list since no item can/should appear twice in names_set
        #             del self.prime_data[index]
        #             break
        return ret

    def _get_primes_data(self) -> list['PrimeItem']:
        data = api_requester.request_prime_data()
        # filter to only contain rewards that have ducat value
        data = dict(filter(self._primes_data_filter, data.items()))
        primes_data = [PrimeItem(item_name, item_data['IsVaulted'], item_data['Parts']) for item_name, item_data in data.items()]
        return primes_data

    def _primes_data_filter(self, pair):
        item_name, dct = pair
        for part_info in dct['Parts'].values():
            if part_info['DucatValue'] <= 0:
                return False
        return True

class PrimeItem:
    def __init__(self, name: str, is_vaulted: bool, parts_data: dict[str, dict], item_id: str = None) -> None:
        self._name = name
        self._is_vaulted = is_vaulted
        self._parts_data = parts_data
        self._item_id = item_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def is_vaulted(self) -> bool:
        return self._is_vaulted
    
    @property
    def item_id(self) -> str:
        return self._item_id
    
    @item_id.setter
    def item_id(self, id: str):
        self._item_id = id
    
    def total_dacats_value(self) -> int:
        ducat_value = 0
        for part in self._parts_data.values():
            ducat_value += part['DucatValue']
        return ducat_value
