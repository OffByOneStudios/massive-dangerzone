"""wrapgen.py
@OffbyOneStudios 2013
Code To generated Python "Headers" from Madz Plugin Descriptions.
"""

class PythonGenerator(object):
    """Class to Generate C wrapper for python plugins."""

    def __init__(self, dependencies, namespace, description):
        self.dependencies = dependencies
        self.namespace = namespace
        self.declarations = description.declarations
        self.variables = description.variables


    def make_madz_c_header(self):
        """Returns String of C Header Component."""
        pass

    def python_wrapper_from_struct(self, struct):
        """Generates Python Glue for accessing structs"""

        def make_pyobject(struct):
            """Construct a PyObject struct.
            This struct's members contain dummy PyObject variables for each member in struct.
            Additionally they contain a pointer to struct.
            """

        def make_new(struct):
            """Create Function to Perfom Tp_alloc on the pyObject struct."""
            pass

        def make_dealloc(struct):
            """Constructs dealloc code for PyObject"""
            pass

        def make_init(struct):
            """Creates C description for the class's python constructor."""
            pass

        def make_hidden_dealloc(struct):
            """Creates method on PyObject that can free the object's hidden struct pointer.

            This is used if you need to deallocate the incoming struct from madz from python.
            """
            pass

        def make_method_table(struct):
            """Creates a method table for the PyObject.
            This will only include the hidden dealloc method in the case of regular structs.
            This will also contain methods that wrap function pointers attached to dependant modules.
            """
            pass

        def make_attr_functions(struct):
            """Creates custom getattr/setattr methods for object.

            These methods intercept class property read/writes and redirects them to the hidden struct.

            """
            pass

        def make_python_type_array(struct):
            """Fills in PyTypeObject array with the above functions."""
            pass

        def wrap_struct_function_pointers(struct):
            """wraps any function pointers associated with struct (like when a plugin is included as a dependency)
            and creates PyObjects from their results.
            """

    def make_plugin_functions(self):
        """Creates functions associated with the actual functions described in the interface.
        These box incomming types into python, call the python function associated with the module, and unbox results.
        """
        pass

    def make_module_init(self):
        """Creates function to bind a python module to this interface description.

        This module must contain matching names for the functions described in the plugin description
        """
        pass
