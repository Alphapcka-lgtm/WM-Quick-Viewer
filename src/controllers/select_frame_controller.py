from models.warframe_market_model import WarframeMarketData
from models.market_item import MarketItem
from utils.observable_dict import ObservableDict
from views.select_frame import SelectFrame
from tkinter.messagebox import showerror
from pywmapi.common.enums import Language
import tkinter as tk

class SelectFrameController():
    def __init__(self, model: WarframeMarketData, frame: SelectFrame) -> None:
        self.model = model
        self.frame = frame

        lang = next(iter(self.model.langs))
        names = self.model.item_names_excluded(lang)
        self.frame.items_var.set(names)
        
        self._config_elements()
        self._bind()

    def _config_elements(self):
        langs = self.model.langs
        self.frame.lang_combo.config(values=[lang.value for lang in langs])
        self.frame.lang_combo.current(0)
        lang = Language(self.frame.lang_combo.get())
        self.model.current_lang = lang

        self.frame.items_lb.config(selectmode=tk.SINGLE)

        vcmd = (self.frame.multiplier_entry.register(self._multiplier_input_validation))
        self.frame.multiplier_entry.config(validatecommand=(vcmd, '%P'))

        vcmd = (self.frame.quantity_entry.register(self._quantity_input_validation))
        self.frame.quantity_entry.config(validatecommand=(vcmd, '%P'))

        vcmd = (self.frame.items_search_entry.register(self._item_search))
        self.frame.items_search_entry.config(validatecommand=(vcmd, '%P'))
    
    def _bind(self):
        self.frame.btn_add.config(command=self._add_btn_command)
        self.frame.lang_combo.bind('<<ComboboxSelected>>', self._on_lang_select)
        self.frame.items_lb.bind('<<ListboxSelect>>', self._on_item_select)

    def _on_item_select(self, event):
        curseselection: tuple[str, ...] = self.frame.items_lb.curselection()
        if len(curseselection) == 0:
            self.frame.btn_add.config(state='disabled')
            return
        
        self.frame.btn_add.config(state='normal')

    def _on_lang_select(self, event):
        lang_str = self.frame.lang_combo.get()
        lang = Language(lang_str)
        self.model.current_lang = lang
        self.frame.items_var.set(self.model.item_names(lang))

    def _item_search(self, _: str) -> bool:
        search_input = self.frame.items_search_entry.get()
        names = self.model.item_names(Language(self.frame.lang_combo.get()))
        if search_input == '':
            self.frame.items_var.set(names)
        else:
            filtered_names = list(filter(lambda item_name: search_input in item_name, names))
            self.frame.items_var.set(filtered_names)
        
        return True
    
    def _multiplier_input_validation(self, after: str):
        if after.replace(',', '').replace('.', '').isnumeric():
            return True
        return False

    def _quantity_input_validation(self, P: str):
        if P.isdigit() or P == '':
            return True
        return False

    def _add_btn_command(self):
        try:
            multiplier = float(self.frame.multiplier_entry.get())
        except ValueError:
            multiplier = 1.0
            showerror('Input Error', 'Error when converting multiplier.\nContinuing with a multiplier of 1.0')

        quantity = self.frame.quantity_entry.get()
        if not quantity or not quantity.isdigit():
            quantity = 1
        else: quantity = int(quantity)
        
        lang_str = self.frame.lang_combo.get()
        lang = Language(lang_str)

        curse_sel = self.frame.items_lb.curselection()[0]
        item_name = self.frame.items_var.get()[curse_sel]
        item_id = self.model.name_to_id(item_name, lang)

        self.model.add_selected(item_id, quantity, multiplier) 

        self.frame.items_var.set(self.model.item_names_excluded(self.model.current_lang))
    
    def _on_selected_items_changed(self, mode: str, item_id: str, item: MarketItem):
        names = self.model.item_names_excluded(self.model.current_lang)
        self.frame.items_var.set(names)
