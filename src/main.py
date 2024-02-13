from pywmapi.common.enums import Language
from views.select_frame import SelectFrame
# from views._old_selected_list_frame import SelectedListFrame
from views.selected_view import SelectedView
from views.plot_frame import PlotFrame
from models.warframe_market_model import WarframeMarketData

from controllers.select_frame_controller import SelectFrameController
from controllers.selected_view_controller import SelectedViewController

import tkinter as tk

from views.item_view import ItemView
import pywmapi
from models.market_item import MarketItem


def main():
    LANGS = {Language.en, Language.de}

    app = tk.Tk()
    app.title('Warframe.Market App-Dings')
    img = tk.PhotoImage(file='./warframe-market_icon.png')
    app.iconphoto(True, img)
    app.geometry('600x350')

    print('requesting item data... ', end='')
    data = WarframeMarketData(LANGS)
    print('done')
    select_frame = SelectFrame(app)
    select_frame_controller = SelectFrameController(data, select_frame)
    selected = SelectedView(app)
    selected_controller = SelectedViewController(selected, data)
    plot_frame = PlotFrame(app)

    select_frame.grid(column=0, row=0, sticky='w')
    selected.grid(column=1, row=0, sticky='w')
    plot_frame.grid(column=0, columnspan=2, row=1, sticky='we')

    app.columnconfigure(1, weight=1)
    app.rowconfigure(1, weight=1)

    app.mainloop()

def item_view_test_display():
    app = tk.Tk()
    app.title('Test item view')
    app.geometry('350x80')

    short = pywmapi.items.list_items()[0]
    item = MarketItem(short)
    item.set_lang_name(Language.en, short.item_name)
    view = ItemView(app, item)
    view.pack(fill='both')

    app.mainloop()

if __name__ == '__main__':
    main()
    # item_view_test_display()