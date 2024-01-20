from pywmapi.common.enums import Language
from select_frame import SelectFrame
from plot_frame import PlotFrame
import warframe_market_data
import tkinter as tk


def main():
    LANGS = [
        Language.en,
        Language.de,
    ]

    app = tk.Tk()
    app.title('Warframe.Market App-Dings')
    img = tk.PhotoImage(file='./warframe-market_icon.png')
    app.iconphoto(True, img)
    app.geometry('450x350')

    items_lang_dict = warframe_market_data.get_items_lang_dict(LANGS)
    select_frame = SelectFrame(items_lang_dict, app, LANGS)
    plot_frame = PlotFrame(app)
    select_frame.register_plot_frame(plot_frame)

    select_frame.pack(fill=tk.BOTH)
    plot_frame.pack(fill=tk.BOTH)

    app.mainloop()


if __name__ == '__main__':
    main()