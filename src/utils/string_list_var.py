from typing import Iterable
from tkinter import Misc, StringVar, Variable

class ListStringVar(Variable):
    def __init__(self, master: Misc | None = None, value: str | None = None, name: str | None = None) -> None:
        Variable.__init__(self, master, value, name)
    
    def set(self, elements: Iterable[str]):
        return self._tk.globalsetvar(self._name, elements)
    
    def add(self, element: str):
        self._tk.globalgetvar(self._name).append(element)
    
    def get(self) -> list[str]:
        return list(self._tk.globalgetvar(self._name))
