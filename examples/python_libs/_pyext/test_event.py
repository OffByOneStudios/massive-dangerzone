import unittest
import functools

import pyext

# Monkey patchable object
class Example(object):
    pass
exmp = Example()

class TestException(Exception): pass

def throws(*args):
    raise TestException("Test")

@functools.total_ordering
class SortedCallable(object):
    def __init__(self, order, callback):
        self._order = order
        self._call = callback

    def __call__(self, *args, **kwargs):
        return self._call(*args, **kwargs)

    def __gt__(self, other):
        return self._order > other._order

    def __eq__(self, other):
        return self._order == other._order

class PyExt_Event(unittest.TestCase):
    """Events are basically just lists of callbacks."""
    
    def test_0_construct_event(self):
        """So their construction is simple."""
        
        exmp.simple = pyext.Event()

        # A named event:
        exmp.named = pyext.Event(name="foo")

        # A sorted event:
        exmp.sortable = pyext.Event(sort=sorted)

        # A fail event:
        exmp.fails = pyext.Event(fails=True)
    
    def test_1_add_handler(self):
        """The event library overloads the += syntax to add handlers."""
        def assign(v):
            exmp.res = v
        
        exmp.simple += lambda arg: assign(arg)
        exmp.named += assign
        exmp.fails += assign
        exmp.sortable += SortedCallable(0, lambda arg: assign([]))
        exmp.sortable += SortedCallable(1, lambda arg: exmp.res.append(arg))

    def test_2_call(self):
        """The event library overloads call to invoke the events."""
        exmp.simple("test")
        self.assertEqual(exmp.res, "test")
        
        exmp.named("name test")
        self.assertEqual(exmp.res, "name test")
        
        exmp.sortable("sort test").exceptions
        self.assertListEqual(exmp.res, ["sort test"])
        
        exmp.fails("fails test")
        self.assertEqual(exmp.res, "fails test")
        
    def test_3_advanced_returns(self):
        """Calling an event returns a list of the callback results."""
        exmp.ident = lambda arg: arg
        exmp.simple += exmp.ident

        result = exmp.simple("testing_arg")
        self.assertIn("testing_arg", result.returns)

    def test_4_call_failure(self):
        """The event library ensures the exceptions stops at it's boundry."""
        exmp.simple += throws
        result = exmp.simple("test")
        self.assertEqual(len(result.exceptions), 1)
        self.assertIsInstance(list(result.exceptions)[0], TestException)

        # unless we ask it to fail:
        exmp.fails += throws
        self.assertRaises(TestException, exmp.fails, "test")

    def test_5_length(self):
        """The event library provides the length of the callback list."""
        self.assertEqual(len(exmp.simple), 3)
        self.assertEqual(len(exmp.fails), 2)
        self.assertEqual(len(exmp.sortable), 2)
        self.assertEqual(len(exmp.named), 1)

    def test_6_contains(self):
        """We can also test to see if a callback is in the event."""
        self.assertIn(throws, exmp.simple)
        self.assertIn(throws, exmp.fails)
        self.assertIn(exmp.ident, exmp.simple)

    def test_7_remove(self):
        """The event library overloads -= to remove specific events."""
        exmp.simple -= throws
        self.assertEqual(len(exmp.simple), 2)
        
        exmp.simple -= exmp.ident
        self.assertEqual(len(exmp.simple), 1)

        # Can't remove the same event twice:
        self.assertRaises(pyext.MissingEventHandler, exmp.simple.__isub__, exmp.ident)

        # Unless we add it twice, it would also be called twice
        exmp.fails += throws
        self.assertEqual(len(exmp.fails), 3)
        
        exmp.fails -= throws
        self.assertEqual(len(exmp.fails), 2)
        
        exmp.fails -= throws
        self.assertEqual(len(exmp.fails), 1)
