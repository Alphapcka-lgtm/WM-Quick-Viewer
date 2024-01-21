from pywmapi.common.enums import Language
from select_frame import SelectFrame
from selected_list_frame import SelectedListFrame
from plot_frame import PlotFrame
import warframe_market_data
import tkinter as tk


def main():
    LANGS = [Language.en, Language.de]

    app = tk.Tk()
    app.title('Warframe.Market App-Dings')
    img = tk.PhotoImage(file='./warframe-market_icon.png')
    app.iconphoto(True, img)
    app.geometry('600x350')

    print('requesting item data... ', end='')
    items_lang_dict = warframe_market_data.get_items_lang_dict(LANGS)
    print('done')
    select_frame = SelectFrame(items_lang_dict, app, LANGS)
    selected = SelectedListFrame(app)
    plot_frame = PlotFrame(app)
    select_frame.register_plot_frame(plot_frame)

    # empty_frame.pack(side='top')
    # select_frame.pack(side='left', fill='y')
    # selected.pack(side='right', fill='y')
    # plot_frame.pack(side='bottom', fill='y')

    select_frame.grid(column=0, row=0, sticky='w')
    selected.grid(column=1, row=0, sticky='w')
    plot_frame.grid(column=0, columnspan=2, row=1, sticky='we')

    app.columnconfigure(1, weight=1)
    app.rowconfigure(1, weight=1)

    app.mainloop()


if __name__ == '__main__':
    main()
