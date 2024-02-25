from pywmapi.common.enums import Language

from views.lang_select_view import LangSelectView
from views.select_frame import SelectFrame
from views.selected_view import SelectedViewTV, SelectedView
from views.plot_frame import PlotFrame
from models.warframe_market_model import WarframeMarketData

from controllers.lang_select_controller import LangSelectController
from controllers.select_frame_controller import SelectFrameController
from controllers.selected_view_controller import SelectedViewController, SelectedViewTVController
from controllers.plot_frame_controller import PlotFrameController

import tkinter as tk
from tkinter import ttk

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
    # lang_frame.config(highlightbackground='blue', highlightthickness=2, borderwidth=0)
    lang_frame_controller = LangSelectController(data, lang_frame)
    # lang_frame.grid(column=0, row=0, sticky='WE', columnspan=2)

    select_frame = SelectFrame(app)
    select_frame.config(highlightbackground='red', highlightthickness=2, borderwidth=0)
    # select_frame.config(width=50, height=50)
    select_frame_controller = SelectFrameController(data, select_frame)
    # select_frame.grid(column=0, row=1, sticky='NWE')

    # selected = SelectedView(app)
    # selected.config(highlightbackground='green', highlightthickness=2, borderwidth=0)
    # selected.config(width=50, height=50)
    # selected_controller = SelectedViewController(selected, data)
    # selected.grid(column=1, row=1, sticky='NWE')
    selected = SelectedViewTV(app)
    selected_controller = SelectedViewTVController(selected, data)

    plot_frame = PlotFrame(app)
    # plot_frame.config(width=50, height=50)
    plot_frame.config(highlightbackground='yellow', highlightthickness=2, borderwidth=0)
    plotframe_controller = PlotFrameController(data, plot_frame)
    # plot_frame.grid(column=0, row=2, sticky='WES', columnspan=2)

    selected_controller.plot_frame_controller = plotframe_controller

    app.columnconfigure(0, weight=1)
    app.columnconfigure(1, weight=1)
    app.rowconfigure(0, weight=0)
    app.rowconfigure(1, weight=1)

    lang_frame.grid(column=0, row=0, sticky='NSEW', columnspan=2)
    select_frame.grid(column=0, row=1, sticky='NSEW', pady=10)
    selected.grid(column=1, row=1, sticky='NSEW', pady=10)
    plot_frame.grid(column=0, row=2, sticky='NSEW', columnspan=2)

    app.columnconfigure(1, weight=1)
    app.rowconfigure(1, weight=1)

    app.mainloop()

if __name__ == '__main__':
    main()
    # origin = 'https://warframe.fandom.com'
    # path = '/api.php'
    # params = {
	#     'action': "scribunto-console",
	#     'format': "json",
	#     'title': "Module:Void/data",
	#     'content': "",
	#     'question': 'local VoidData = require(\'Module:Void/data\').PrimeData local json = require(\'Module:JSON\') print(json.stringify(VoidData))',
	#     'clear': '1'
    # }
    # query_string = urlencode(params)
    # url = f"{origin}{path}?{query_string}"
    # print(url)
