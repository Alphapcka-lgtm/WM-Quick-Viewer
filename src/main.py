from select_frame import SelectFrame
from plot_frame import PlotFrame
import tkinter as tk
import warframe_market_data
import pywmapi

def main():
    app = tk.Tk()
    app.title('Warframe.Market App-Dings')
    app.geometry('450x300')

    items_dict = warframe_market_data.get_items_dict(pywmapi.common.enums.Language.de)
    select_frame = SelectFrame(items_dict, app)
    plot_frame = PlotFrame(app)
    select_frame.register_plot_frame(plot_frame)

    select_frame.pack(fill=tk.BOTH)
    plot_frame.pack(fill=tk.BOTH)

    app.mainloop()

if __name__ == '__main__':
    main()
