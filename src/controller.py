from warframe_market_data import WarframeMarketData

class Controller():

    def __init__(self, data: WarframeMarketData) -> None:
        self._data = data

    @property
    def data(self):
        return self._data

    