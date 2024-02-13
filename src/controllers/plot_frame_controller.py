from ..models.warframe_market_model import WarframeMarketData
from ..views.plot_frame import PlotFrame

class PlotFrameController():
    def __init__(self, model: WarframeMarketData, view: PlotFrame) -> None:
        self.model = model
        self.view = view
        # self.rm_listener_func = self.model.add_event_listener('on_get_item', self._on_get_item)

    def _on_get_item(self, model: WarframeMarketData, item):
        pass
