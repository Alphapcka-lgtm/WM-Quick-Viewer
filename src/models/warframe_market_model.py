import pywmapi
from pywmapi.common.enums import Language
from models.market_item import MarketItem
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
        item.statistics = pywmapi.statistics.get_statistic(item.url_name)
        item.orders = pywmapi.orders.get_orders(item.url_name)
        self.selected_items[item_id] = item
    
    def rmv_selected(self, item_id: str):
        self.items_dict.pop(item_id)
        
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
