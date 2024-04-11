from views.lang_select_view import LangSelectView
from models import WarframeMarketData
from pywmapi.common.enums import Language

class LangSelectController:
    def __init__(self, model: WarframeMarketData, view: LangSelectView) -> None:
        self.model = model
        self.view = view

        langs_str = [lang.value for lang in self.model.langs]
        self.view.lang_cmb.config(values=langs_str)
        self.view.lang_cmb.current(0)
        self.view.lang_cmb.bind('<<ComboboxSelected>>', self._on_lang_select)
        
        lang = Language(self.view.lang_cmb.get())
        self.model.current_lang = lang
    
    def _on_lang_select(self, event):
        lang_str = self.view.lang_cmb.get()
        lang = Language(lang_str)
        self.model.current_lang = lang
