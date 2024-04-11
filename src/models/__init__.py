import pywmapi
from pywmapi.items.models import ItemShort
from pywmapi.statistics.models import Statistic
from pywmapi.orders.models import OrderRow
from pywmapi.common.enums import Language

import api_requester
from typing import Callable
from utils.observable_dict import ObservableDict


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

    def get_lang_name(self, lang: Language):
        return self.localized_item_names.get(lang.value, None)

    def set_lang_name(self, lang: Language, name: str):
        self.localized_item_names[lang.value] = name
    
    def remove_lang_name(self, lang: Language):
        self.localized_item_names.__delitem__(lang.value)
