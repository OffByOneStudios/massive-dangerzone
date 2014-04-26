import unittest

import pyext

# Monkey patchable object
class Example(object):
    pass
exmp = Example()

class PyExt_Context(unittest.TestCase):
    """Contexts are basically just global variables."""
    
    def test_0_construct_var(self):
        """To use a context variable we must first construct it. This is done
        by passing the ContextVariable function a key to use as the variable's
        symbol."""
        
        self.assertRaises(Exception, pyext.ContextVariable)
        
        exmp.foo_var = pyext.ContextVariable("foo")
        
        # Often best if they are associated with a unique python symbol:
        exmp.our_var = pyext.ContextVariable(PyExt_Context)
        
        # We can also assign a default value:
        exmp.bar_var = pyext.ContextVariable("bar", 15)
    
    def test_1_retrieve_var(self):
        """We can now retrieve variables from the context system."""
        self.assertEqual(exmp.foo_var, pyext.get_variable("foo"))
        self.assertEqual(exmp.our_var, pyext.get_variable(PyExt_Context))
        self.assertRaises(pyext.MissingContextVariableError, pyext.get_variable, "does not exist")
        
        # we can also use this function create a new variable if we set the safe parameter
        exmp.baz_var = pyext.get_variable("baz", safe=True)
    
    def test_2_destroy_var(self):
        """Variables can be destroyed."""
        
        exmp.our_var.destroy()
        self.assertRaises(pyext.MissingContextVariableError, pyext.get_variable, PyExt_Context)
    
    def test_3_set_value(self):
        """Context variables store a value, we can set this value using the set function."""
        exmp.foo_var.set({"var": exmp.foo_var})
    
    def test_4_get_value(self):
        """Context variables store a value, we can get this value using the get function."""
        self.assertEqual(exmp.bar_var.get(), 15)
        self.assertEqual(exmp.foo_var.get()["var"], exmp.foo_var)
        # Value defaults to None
        self.assertEqual(exmp.baz_var.get(), None)
    
    def test_5_with_value(self):
        """We can also use with to change the value of the varibles temporarily."""
        self.assertEqual(exmp.bar_var.get(), 15)
        with exmp.bar_var.set_to(12):
            self.assertEqual(exmp.bar_var.get(), 12)
        self.assertEqual(exmp.bar_var.get(), 15)
        
        # Even through exceptions:
        try:
            with exmp.bar_var.set_to(8):
                self.assertEqual(exmp.bar_var.get(), 8)
                raise Exception()
        except Exception:
            pass
        self.assertEqual(exmp.bar_var.get(), 15)
    
    def test_6_collect(self):
        """We can use helper functions to collect the current context variable state, and then reapply it."""
        self.assertEqual(exmp.bar_var.get(), 15)
        context = pyext.collect_context()
        
        exmp.bar_var.set(30)
        self.assertEqual(exmp.bar_var.get(), 30)
        
        pyext.expand_context(context)
        self.assertEqual(exmp.bar_var.get(), 15)
        
        # Also using with statements:
        exmp.baz_var.set(True)
        self.assertEqual(exmp.baz_var.get(), True)
        with pyext.the_context(context):
            self.assertEqual(exmp.baz_var.get(), None)
            # The next stament is thrown away with the resumption of the context
            exmp.baz_var.set(False)
            # But this new variable isn't:
            temp_var = pyext.ContextVariable("temp_example", "still here")
        self.assertEqual(exmp.baz_var.get(), True)
        self.assertEqual(temp_var.get(), "still here")
        
        temp_var.destroy()
    