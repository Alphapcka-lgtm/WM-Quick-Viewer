from warframe_market_data import WarframeMarketData
from select_frame import SelectFrame
from selected_list_frame import SelectedListFrame
from plot_frame import PlotFrame
from tkinter.messagebox import showerror

class Controller():

    def __init__(self, data: WarframeMarketData) -> None:
        self._data = data
        self.select_frame: SelectFrame = None
        self.selected_list_frame: SelectedListFrame = None
        self.plot_frame: PlotFrame = None

    @property
    def data(self):
        return self._data
    
    def notify_price_btn(self):
        if self.selected_list_frame == None:
            showerror('Controller Error', 'No selected list frame has been registered!')
            return
        if self.plot_frame == None:
            showerror('Controller Error', 'No plot frame has been registered!')
            return
        if self.select_frame == None:
            showerror('Controller Error', 'No select frame has been registered!')
            return
        
        selected_items = self.selected_list_frame.get_selected()
        # TODO

    def register_select_frame(self, select_frame: SelectFrame):
        self.select_frame = select_frame
    
    def register_selected_list_frame(self, selected_list_frame: SelectedListFrame):
        self.selected_list_frame = selected_list_frame
    
    def register_plot_frame(self, plot_frame: PlotFrame):
        self.plot_frame = plot_frame
