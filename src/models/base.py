import enum

class ObservableModel:
    def __init__(self) -> None:
        self._event_listeners = {}
    
    def add_event_listener(self, event, func):
        """
        Add an event listener to the observabel controller.

        Parameters
        ----------
        event: The event on which the listener should be triggered.
        func: The function that will be called when the event is triggered.

        Returns
        -------
        A function to remove the listener.
        """
        if event in self._event_listeners.keys():
            self._event_listeners[event].append(func)
        else:
            self._event_listeners[event] = [func]
    
        return lambda: self._event_listeners[event].remove(func)

    def trigger_event(self, event):
        if event not in self._event_listeners.keys():
            return
        
        for func in self._event_listeners[event]:
            func(self)
