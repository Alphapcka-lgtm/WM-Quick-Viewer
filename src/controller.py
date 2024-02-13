from models.warframe_market_model import WarframeMarketData
# import select_frame as sf
# import selected_list_frame as slf
# from plot_frame import PlotFrame


class Controller():

    def __init__(self, data: WarframeMarketData) -> None:
        self._data = data
        self.select_frame = None
        self.selected_list_frame = None
        self.plot_frame = None

    @property
    def data(self):
        return self._data

    def register_select_frame(self, select_frame):
        self.select_frame = select_frame
    
    def register_selected_list_frame(self, selected_list_frame):
        self.selected_list_frame = selected_list_frame
    
    def register_plot_frame(self, plot_frame):
        self.plot_frame = plot_frame
