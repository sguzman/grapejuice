class Event:
    def __init__(self):
        self._listeners = []

    def add_listener(self, listener: callable):
        assert callable(listener), "The given listener must be callable"
        self._listeners.append(listener)

    def remove_listener(self, listener):
        if listener in self._listeners:
            self._listeners.remove(listener)

    def __call__(self, *args, **kwargs):
        for listener in self._listeners:
            listener(*args, **kwargs)
