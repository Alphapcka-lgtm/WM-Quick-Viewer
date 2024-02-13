from models.warframe_market_model import WarframeMarketData
from views.item_view import ItemView

class ItemViewController:
    def __init__(self, view: ItemView, data: WarframeMarketData) -> None:
        self.data = data
        self.frame = view
