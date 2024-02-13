from typing import TypeVar, Callable, overload

_T = TypeVar('_T')
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


class ObservableDict(dict[_KT, _VT]):

    ITEM_ADDED = 'add'
    ITEM_DEL = 'del'

    def __new__(cls):
        cls._listeners: list[Callable[[str, _KT, _VT], None]] = []
        return super().__new__(cls)

    def __init_subclass__(cls) -> None:
        cls._listeners: list[Callable[[str, _KT, _VT], None]] = []
        return super().__init_subclass__(cls)
    
    def add_listener(self, func: Callable[[str, _KT, _VT], None]):
        self._listeners.append(func)
        return lambda: self._listeners.remove(func)
    
    def popitem(self) -> tuple[_KT, _VT]:
        key, val = super().popitem()
        [func(self.ITEM_DEL, key, val) for func in self._listeners]
        return key, val
    
    @overload
    def pop(self, __key: _KT) -> _VT: ...
    @overload
    def pop(self, __key: _KT, __default: _VT = None) -> _VT: ...
    def pop(self, __key: _KT, __default: _T = None) -> _VT | _T:
        if __default:
            val = super(ObservableDict, self).pop(__key, __default)
        else: 
            val = super(ObservableDict, self).pop(__key)
        [func(self.ITEM_DEL, __key, val) for func in self._listeners]
        return val
    
    def __setitem__(self, __key: _KT, __value: _VT) -> None:
        super(ObservableDict, self).__setitem__(__key, __value)
        [func(self.ITEM_ADDED, __key, __value) for func in self._listeners]
    
    def __delitem__(self, __key: _KT) -> None:
        val = self[__key]
        super(ObservableDict, self).__delitem__(__key)
        [func(self.ITEM_DEL, __key, val) for func in self._listeners]
