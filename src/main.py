from tkinter import ttk, messagebox
import tkinter as tk
import pywmapi
import statistics
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pprint import pformat


XELTO_MODIFIER = 0.60

def main():
    app = tk.Tk()
    app.title('Warframe.Market App-Dings')
    app.geometry('450x300')

    items_short = pywmapi.items.list_items(pywmapi.common.enums.Language.de)
    items_dict = {item.item_name: item for item in items_short}

    # with open('f.txt', 'w', encoding='UTF-8') as _file:
    #     _file.write(pformat(items_dict))

    select_frame = tk.Frame(app)

    tk.Label(select_frame, text='Wähle das Item:').grid(column=0, row=0, padx=10, sticky='W')

    items_combo = ttk.Combobox(select_frame, width=30)
    items_combo.config(textvariable=tk.StringVar())
    items_combo['values'] = list(items_dict.keys())

    def on_select(event: tk.Event):
        if event.widget.get() == '':
            btn.config(state='disabled')
        else: 
            btn.config(state='normal')
    items_combo.bind('<<ComboboxSelected>>', on_select)

    def check_item_combo_input(event):
        value:str = event.widget.get()

        if value == '':
            items_combo['values'] = list(items_dict.keys())
        else:
            items_combo['values'] = [item for item in items_dict.keys() if value.lower() in item.lower()]
    items_combo.bind('<KeyRelease>', check_item_combo_input)
    items_combo.grid(column=0, row=1, padx=10, sticky='W')

    tk.Label(select_frame, text='Gib die Anzahl ein:').grid(column=1, row=0, padx=10, sticky='W')

    def validate_quantity_entry(P: str):
        if P.isdigit() or P == '':
            return True
        return False
    quantity_entry = tk.Entry(select_frame, validate='key', width=5)
    quantity_entry.insert(0, '1')
    vcmd = (quantity_entry.register(validate_quantity_entry))
    quantity_entry.config(validatecommand=(vcmd, '%P'))
    quantity_entry.grid(column=1, row=1, padx=10, sticky='W')

    tk.Label(select_frame, text='Multiplier:').grid(column=2, row=0, padx=10, sticky='W')
    tv = tk.DoubleVar()
    price_mulitplier_entry = tk.Entry(select_frame, validate='key', width=5, textvariable=tv)
    tv.set(XELTO_MODIFIER)
    # discount_entry.insert(0, 60)
    def validate_discount_entry(after: str):
        if after.replace(',', '').replace('.', '').isnumeric():
            return True
        return False
    vcmd = (price_mulitplier_entry.register(validate_discount_entry))
    price_mulitplier_entry.config(validatecommand=(vcmd, '%P'))
    price_mulitplier_entry.grid(column=2, row=1, padx=10, sticky='W')

    # spacer grid
    tk.Label(select_frame).grid(column=1, row=2)

    def btn_command():
        try:
            multiplier = float(price_mulitplier_entry.get())
        except ValueError:
            messagebox.showerror('Input Error', 'Error when converting multiplier!')
            return
        selected_item = items_combo.get()
        item_short = items_dict[selected_item]
        orders = pywmapi.orders.get_orders(item_short.url_name)
        orders = list(filter(lambda order: order.order_type == pywmapi.orders.OrderType.sell and order.user.status == pywmapi.auth.models.UserShort.Status.ingame , orders))
        prices_per_one = list(map(lambda order: order.platinum / order.quantity, orders))
        mean_single_price = round(statistics.mean(prices_per_one))

        label_single_price.config(text=f'Durchschnittspreis pro item: {mean_single_price} Platin')
        label_multiplier_single_price.config(text=f'Multiplier Preis pro Item: {round(mean_single_price * multiplier)} Platin')

        quantity = quantity_entry.get()

        if not quantity.isdigit() or quantity == '' or int(quantity) == 1:
            label_quantity_price.config(text='')
            label_multiplier_quantity_price.config(text='')
        else:
            label_quantity_price.config(text=f'Preis für {int(quantity)} Items: {mean_single_price * int(quantity)} Platin')
            label_multiplier_quantity_price.config(text=f'Multiplierer Preis für {int(quantity)} Items: {round(mean_single_price * int(quantity) * multiplier)} Platin')

        # with open('orders.txt', 'w+', encoding='UTF-8') as _file:
        #     _file.write(pformat(prices_per_one) + f'\nDurchschnitts Preis für einmal: {mean_single_price}')
    btn = tk.Button(select_frame, text='confirm', width=10, state='disabled', command=btn_command)
    btn.grid(column=1, row=3, padx=10, sticky='W')

    # spacer grids
    tk.Label(select_frame).grid(column=1, row=3)
    tk.Label(select_frame).grid(column=1, row=4)

    label_single_price = tk.Label(select_frame)
    label_single_price.grid(column=0, row=5, padx=10, sticky='W')

    label_quantity_price = tk.Label(select_frame)
    label_quantity_price.grid(column=1, row=5, padx=10, sticky='W')

    label_multiplier_single_price = tk.Label(select_frame)
    label_multiplier_single_price.grid(column=0, row=6, padx=10, sticky='W')

    label_multiplier_quantity_price = tk.Label(select_frame)
    label_multiplier_quantity_price.grid(column=1, row=6, padx=10, sticky='W')

    select_frame.pack(fill=tk.BOTH)

    plot_frame = tk.Frame(app)
    f = Figure(figsize=(5, 5), dpi=100)
    a = f.add_subplot(111)
    a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

    canvas = FigureCanvasTkAgg(f, plot_frame)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

    toolbar = NavigationToolbar2Tk(canvas, plot_frame)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    plot_frame.pack(fill=tk.BOTH)

    app.mainloop()

if __name__ == '__main__':
    item_statistics = pywmapi.statistics.get_statistic('arcane_ice')
    # with open('stat.txt', 'w+', encoding='utf-8') as _file:
    #     _file.write(pformat(item_statistics.closed_48h) + '\n\n' + pformat(item_statistics.live_48h))

    main()
