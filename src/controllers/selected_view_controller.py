from views.selected_view import SelectedView
from views.item_view import ItemView
from models.warframe_market_model import WarframeMarketData
from models.market_item import MarketItem
from utils.observable_dict import ObservableDict
from controllers.item_view_controller import ItemViewController
from controllers.plot_frame_controller import PlotFrame

class SelectedViewController:
    def __init__(self, view: SelectedView, model: WarframeMarketData) -> None:
        self.frame = view
        self.model = model
        self.model.selected_items.add_listener(self._on_item_selected)

        self._selected_views: dict[str, tuple[ItemView, ItemViewController]] = {}

        self._pf_ctrl: PlotFrame = None
    
    @property
    def plot_frame_controller(self):
        return self._pf_ctrl
    
    @plot_frame_controller.setter
    def plot_frame_controller(self, ctlr: PlotFrame):
        self._pf_ctrl = ctlr

    def _on_item_selected(self, mode: str, item_id: str, item: MarketItem):
        if mode == ObservableDict.ITEM_ADDED:
            interior = self.frame.items_frame.interior
            item_view = ItemView(interior)
            item_view.pack(side='bottom')


            iv_ctrl = ItemViewController(item_view, self.model, item)
            iv_ctrl.plot_frame_controller = self.plot_frame_controller
            
            self._selected_views[item_id] = (item_view, iv_ctrl)
            # interior.pack()
            # tk.Label(interior, text='is was just added!').pack()
        else:
            item_view, item_view_ctrl = self._selected_views[item_id]
            item_view.destroy()
            item_view_ctrl.rm_lang_listener()
            
            del item_view
            del item_view_ctrl
