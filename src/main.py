from pywmapi.common.enums import Language

from views.lang_select_view import LangSelectView
from views.select_frame import SelectFrame
from views.selected_view import SelectedView
from views.plot_frame import PlotFrame
from models.warframe_market_model import WarframeMarketData

from controllers.lang_select_controller import LangSelectController
from controllers.select_frame_controller import SelectFrameController
from controllers.selected_view_controller import SelectedViewController
from controllers.plot_frame_controller import PlotFrameController

import tkinter as tk


def main():
    LANGS = {Language.en, Language.de}

    app = tk.Tk()
    app.title('WM Quickview')
    img = tk.PhotoImage(file='./warframe-market_icon.png')
    app.iconphoto(True, img)
    app.geometry('800x550')

    print('requesting item data... ', end='')
    data = WarframeMarketData(LANGS)
    print('done')
    lang_frame = LangSelectView(app)
    lang_frame_controller = LangSelectController(data, lang_frame)
    # lang_frame.grid(column=0, row=0, sticky='WE', columnspan=2)

    select_frame = SelectFrame(app)
    # select_frame.config(width=50, height=50)
    select_frame_controller = SelectFrameController(data, select_frame)
    # select_frame.grid(column=0, row=1, sticky='NWE')

    selected = SelectedView(app)
    # selected.config(width=50, height=50)
    selected_controller = SelectedViewController(selected, data)
    # selected.grid(column=1, row=1, sticky='NWE')

    plot_frame = PlotFrame(app)
    plot_frame.config(width=50, height=50)
    plotframe_controller = PlotFrameController(data, plot_frame)
    # plot_frame.grid(column=0, row=2, sticky='WES', columnspan=2)

    selected_controller.plot_frame_controller = plotframe_controller

    lang_frame.grid(column=0, row=0, sticky='WE', columnspan=2)
    select_frame.grid(column=0, row=1, sticky='NEW')
    selected.grid(column=1, row=1, sticky='NEW')
    plot_frame.grid(column=0, row=2, sticky='we', columnspan=2)

    app.columnconfigure(1, weight=1)
    app.rowconfigure(1, weight=1)

    app.mainloop()

if __name__ == '__main__':
    main()
