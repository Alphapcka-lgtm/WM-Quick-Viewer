from pywmapi.common.enums import Language

from views.lang_select_view import LangSelectView
from views.select_frame import SelectFrame
from views.selected_frame import SelectedFrameTV
from views.plot_frame import PlotFrame
from views.primes_ducats import PrimesDuctasWindow
from models import WarframeMarketData

from controllers.lang_select_controller import LangSelectController
from controllers.select_frame_controller import SelectFrameController
from controllers.selected_frame_controller import SelectedFrameTVController
from controllers.plot_frame_controller import PlotFrameController
from controllers.primes_ducats_controller import PrimesDuctasWindowController

import tkinter as tk
from tkinter import ttk

LANGS = {Language.en, Language.de}
app = tk.Tk()
data = WarframeMarketData(LANGS)

def main():

    
    app.title('WM Quickview')
    img = tk.PhotoImage(file='./warframe-market_icon.png')
    app.iconphoto(True, img)
    app.geometry('800x550')

    print('requesting item data... ', end='')
    data = WarframeMarketData(LANGS)
    print('done')
    lang_frame = LangSelectView(app)
    lang_frame_controller = LangSelectController(data, lang_frame)

    select_frame = SelectFrame(app)
    select_frame_controller = SelectFrameController(data, select_frame)

    selected = SelectedFrameTV(app)
    selected_controller = SelectedFrameTVController(selected, data)

    plot_frame = PlotFrame(app)
    plotframe_controller = PlotFrameController(data, plot_frame)

    selected_controller.plot_frame_controller = plotframe_controller

    app.columnconfigure(0, weight=1)
    app.columnconfigure(1, weight=1)
    app.rowconfigure(0, weight=0)
    app.rowconfigure(1, weight=1)

    lang_frame.grid(column=0, row=0, sticky='NSEW', columnspan=2)
    select_frame.grid(column=0, row=1, sticky='NSEW', pady=10)
    selected.grid(column=1, row=1, sticky='NSEW', pady=(0, 10), padx=(0, 10))
    plot_frame.grid(column=0, row=2, sticky='NSEW')

    primes_ducats_btn = ttk.Button(app, text='Primes Ducats', command=_btn_cmd)
    primes_ducats_btn.grid(column=0, row=3, sticky='NSEW')

    app.columnconfigure(1, weight=1)
    app.rowconfigure(1, weight=1)

    app.mainloop()

def _btn_cmd():
    view = PrimesDuctasWindow(app)
    ctrl = PrimesDuctasWindowController(data, app)


if __name__ == '__main__':
    main()
