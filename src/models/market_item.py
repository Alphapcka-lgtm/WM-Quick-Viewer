from pywmapi.items.models import ItemShort
from pywmapi.statistics.models import Statistic
from pywmapi.orders.models import OrderRow
from pywmapi.common.enums import Language
from utils.observable_dict import ObservableDict

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
    
    def calculate_price(self) -> tuple[int, int]:
        pass
