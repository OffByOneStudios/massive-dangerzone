"""pyext/event.py
@OffbyOne Studios 2014
A library for creating events with syntactic suger.
"""

class UncallableEventHandler(Exception): pass
class MissingEventHandler(Exception): pass

class Event(object):
    class EventCallResult(object):
        def __init__(self, sort=False):
            self._sort = sort
            self.exceptions = [] if sort else set()
            self.returns = [] if sort else set()
        def _add_exception(self, exception):
            if self._sort:
                self.exceptions.append(exception)
            else:
                self.exceptions.add(exception)
        def _add_result(self, ret):
            if self._sort:
                self.returns.append(ret)
            else:
                self.returns.add(ret)
        def __str__(self):
            return "<event_result: {return_count} returns | {exception_count} exception>".format(
                return_count=len(self.returns),
                exception_count=len(self.exceptions))
        
    def __init__(self, name=None, sort=None, fails=False):
        self.name = name
        self._calls = []
        self._sort = sort
        self._fails = fails
    
    def attach(self, handler):
        if not callable(handler):
            raise UncallableEventHandler("The event handler '{}' is not callable.".format(handler))
        self._calls.append(handler)
        if not (self._sort is None):
            self._calls = self._sort(self._calls)
    
    def detach(self, handler):
        if handler in self._calls:
            self._calls.remove(handler)
        else:
            raise MissingEventHandler("The event handler '{}' is missing, cannot remove.")
    
    def __iadd__(self, other):
        self.attach(other)
        return self
    
    def __isub__(self, other):
        self.detach(other)
        return self
    
    def __call__(self, *args, **kwargs):
        result = Event.EventCallResult()
        for c in self._calls:
            try:
                result._add_result(c(*args, **kwargs))
            except Exception as e:
                result._add_exception(e)
                if self._fails:
                    raise e
        return result

    def __contains__(self, item):
        return item in self._calls

    def __len__(self):
        return len(self._calls)

    def __str__(self):
        return "<event: {anon}'{name}'| {handler_count} handlers>".format(
            anon=("ANON" if self.name is None else ""),
            name=(id(self) if self.name is None else self._name),
            handler_count=len(self._calls))
