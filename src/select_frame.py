import tkinter as tk
from tkinter import Misc, ttk, messagebox
from pywmapi.items import ItemShort
from pywmapi.common.enums import Language
from plot_frame import PlotFrame
from controller import Controller


class SelectFrame(tk.Frame):

    XELTO_MODIFIER = 0.60

    def __init__(self, controller: Controller, master: Misc, langs: list[Language]) -> None:
        super().__init__(master)

        # self.items_lang_dict = items_lang_dict
        self.controller = controller

        self.plot_frame: PlotFrame = None

        tk.Label(self, text='Lang:').grid(column=0, row=0, padx=10, sticky='W')

        self.lang_combo = ttk.Combobox(self, width=5, textvariable=tk.StringVar(), state='readonly')
        self.lang_combo['values'] = list(controller.data.get_langs)
        self.lang_combo.current(0)
        self.lang_combo.bind('<<ComboboxSelected>>', self._on_lang_select)
        self.lang_combo.grid(column=1, row=0, padx=10, sticky='W')

        tk.Label(self, text='Wähle das Item:').grid(column=0, row=1, padx=10, sticky='W')

        self.items_combo = ttk.Combobox(self, width=30)
        self.items_combo.config(textvariable=tk.StringVar())
        self.items_combo['values'] = self.controller.data.get_item_names('en')
        self.items_combo.bind('<<ComboboxSelected>>', self._on_item_select)
        self.items_combo.bind('<KeyRelease>', self._check_combo_item_input)
        self.items_combo.grid(column=0, row=2, padx=10, sticky='W')

        tk.Label(self, text='Anzahl:').grid(column=1, row=1, padx=10, sticky='W')

        self.quantity_entry = tk.Entry(self, validate='key', width=5)
        self.quantity_entry.insert(0, '1')
        vcmd = (self.quantity_entry.register(self._validate_quantity_entry))
        self.quantity_entry.config(validatecommand=(vcmd, '%P'))
        self.quantity_entry.grid(column=1, row=2, padx=10, sticky='W')

        tk.Label(self, text='Multiplier:').grid(column=2, row=1, padx=10, sticky='W')

        tv = tk.DoubleVar()
        self.price_mulitplier_entry = tk.Entry(self, validate='key', width=5, textvariable=tv)
        tv.set(self.XELTO_MODIFIER)
        vcmd = (self.price_mulitplier_entry.register(self._validate_discount_entry))
        self.price_mulitplier_entry.config(validatecommand=(vcmd, '%P'))
        self.price_mulitplier_entry.grid(column=2, row=2, padx=10, sticky='W')

        # spacer grid
        tk.Label(self).grid(column=1, row=3)

        self.confirm_btn = tk.Button(self, text='confirm', width=10, state='disabled', command=self._btn_command)
        self.confirm_btn.grid(column=1, row=4, padx=10, sticky='W')

        # spacer grids
        tk.Label(self).grid(column=1, row=5)

        self.label_single_price = tk.Label(self)
        self.label_single_price.grid(column=0, row=6, padx=10, sticky='W')

        self.label_quantity_price = tk.Label(self)
        self.label_quantity_price.grid(column=1, row=6, padx=10, sticky='W')

        self.label_multiplier_single_price = tk.Label(self)
        self.label_multiplier_single_price.grid(column=0, row=7, padx=10, sticky='W')

        self.label_multiplier_quantity_price = tk.Label(self)
        self.label_multiplier_quantity_price.grid(column=1, row=7, padx=10, sticky='W')

    def _on_item_select(self, event: tk.Event):
        if event.widget.get() == '':
            self.confirm_btn.config(state='disabled')
        else:
            self.confirm_btn.config(state='normal')

    def _check_combo_item_input(self, event: tk.Event):
        value: str = event.widget.get()

        if value == '':
            self.items_combo['value'] = list(self.items_lang_dict.keys())
        else:
            self.items_combo['values'] = [item for item in self.items_lang_dict.keys() if value.lower() in item.lower()]
    
    def _validate_quantity_entry(self, P: str):
        if P.isdigit() or P == '':
            return True
        return False
    
    def _validate_discount_entry(self, after: str):
        if after.replace(',', '').replace('.', '').isnumeric():
            return True
        return False
    
    def _btn_command(self):
        try:
            multiplier = float(self.price_mulitplier_entry.get())
        except ValueError:
            multiplier = 1.0
            messagebox.showerror('Input Error', 'Error when converting multiplier.\nContinuing with a multiplier of 1.')
        selected_lang = self.lang_combo.get()
        selected_item = self.items_combo.get()
        item_short = self.controller.data.get_item(selected_lang, selected_item)
        date_median_price = self.controller.data.get_item_statistics(item_short)
        # price_per_one = warframe_market_data.item_price_from_statistics_or_order(item_short.url_name, date_median_price)
        if date_median_price:
            price_per_one = self.controller.data.calculate_price(list(date_median_price.values())) 
        else: 
            orders = self.controller.data.get_item_orders(item_short)
            price_per_one = self.controller.data.calculate_price(orders) 

        self.label_single_price.config(text=f'Durchschnittspreis pro item: {price_per_one} Platin')
        self.label_multiplier_single_price.config(text=f'Multiplier Preis pro Item: {round(price_per_one * multiplier)} Platin')

        quantity = self.quantity_entry.get()

        if not quantity or not quantity.isdigit() or int(quantity) == 1:
            self.label_quantity_price.config(text='')
            self.label_multiplier_quantity_price.config(text='')
        else:
            self.label_quantity_price.config(text=f'Preis für {int(quantity)} Items: {price_per_one * int(quantity)} Platin')
            self.label_multiplier_quantity_price.config(text=f'Multiplierer Preis für {int(quantity)} Items: {round(price_per_one * int(quantity) * multiplier)} Platin')
        
        self.plot_frame.update_graph(date_median_price)
    
    def _on_lang_select(self, event: tk.Event):
        lang = event.widget.get()
        self.items_combo['values'] = list(self.items_lang_dict[lang].keys())
        self.items_combo.set('')
    
    def register_plot_frame(self, plot_frame: PlotFrame):
        self.plot_frame = plot_frame
