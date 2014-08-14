"""pyext/event.py
@OffbyOne Studios 2014
A library for creating events, that is lists of callables.
"""

class UncallableEventHandler(Exception): pass
class MissingEventHandler(Exception): pass

class EventCallResult(object):
    """A result container, containg both exceptions and results.

    Attributes:
        exceptions: A list of exceptions.
        results: A list of results from event calls.
    """
    def __init__(self):
        self.exceptions = []
        self.returns = []

    def _add_exception(self, exception):
        self.exceptions.append(exception)

    def _add_result(self, ret):
        self.returns.append(ret)

    def __str__(self):
        return "<event_result: {return_count} returns | {exception_count} exception>".format(
            return_count=len(self.returns),
            exception_count=len(self.exceptions))

class Event(object):
    """An event object, that is a collection of callables with helpers.

    Provides the `+=` and `-=` syntax for `attach()` and `detach()`.

    Attributes:
        name: Name of the event.
    """

    def __init__(self, name=None, sort=None, fails=False):
        """Initializes an Event.

        Args:
            name: An optional name for printing and discovery by EventHubs.
            sort: An optional function for sorting lists of callables (executed on add/remove).
            fails: If true, the event will fail immediately on a handler exception (false by default).
        """
        self.name = name
        self._calls = []
        self._sort = sort
        self._fails = fails

    def attach(self, handler):
        """Attach a handler for this event.

        If a `sort` was provided on init, sort may be called, potentially raising it's exceptions.

        Args:
            handler: The handler to attach. Must be a callable.

        Raises:
            UncallableEventHandler: `handler` is not callable.
        """
        if not callable(handler):
            raise UncallableEventHandler("The event handler '{}' is not callable.".format(handler))
        self._calls.append(handler)
        if not (self._sort is None):
            self._calls = self._sort(self._calls)

    def detach(self, handler):
        """Detach a handler for this event.

        Args:
            handler: The handler to detatch. Must be equal to a previously attached event.

        Raises:
            MissingEventHandler: An error occured finding the correct handler to detach.
        """
        if handler in self._calls:
            self._calls.remove(handler)
        else:
            raise MissingEventHandler("The event handler '{}' is missing, cannot remove.")

    def __iadd__(self, other):
        """Calls attach on rhs."""
        self.attach(other)
        return self

    def __isub__(self, other):
        """Calls detach on rhs."""
        self.detach(other)
        return self

    def __call__(self, *args, **kwargs):
        """Calls all the handlers for this event with the given arguments.

        Calls handlers in `sort` order if provided on init. Raises exceptions only if `fails` was true on init and a handler raises an exception.

        Args:
            *args, **kwargs: Forwared to each handler on call.

        Returns:
            An EventCallResult, with the results (and exceptions if `fails`) of the calls.
        """
        result = EventCallResult()
        for c in self._calls:
            try:
                result._add_result(c(*args, **kwargs))
            except Exception as e:
                result._add_exception(e)
                if self._fails:
                    raise e
        return result

    def __contains__(self, item):
        """Checks for a handler in the call list."""
        return item in self._calls

    def __len__(self):
        """Number of handlers."""
        return len(self._calls)

    def __str__(self):
        return "<event: {anon}'{name}'| {handler_count} handlers>".format(
            anon=("ANON" if self.name is None else ""),
            name=(id(self) if self.name is None else self._name),
            handler_count=len(self._calls))
