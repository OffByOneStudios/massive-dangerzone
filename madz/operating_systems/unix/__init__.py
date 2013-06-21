import ctypes
import os

class UnixOperatingSystem(object):
    def __init__(self):
        self.loaded_plugins = {}

    @staticmethod
    def output_file_location(plugin_stub):
        return os.path.join(plugin_stub.directory, "output")

    def load(self, plugin_stub):
        plugin_dll = ctypes.cdll.LoadLibrary(self.output_file_location(plugin_stub))
        
        madz_init = plugin_dll.___madz_init
        madz_init.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p)]

        return_pointer = ctypes.pointer(ctypes.c_void_p)

        dependencies = plugin_stub.dependencies
        requirements = plugin_stub.requires

        dependencies_array = ctypes.c_void_p * len(dependencies)
        requirements_array = ctypes.c_void_p * len(requirements)

        # TODO(Mason): assign values into arrays

        error_val = madz_init(dependencies_array, requirements_array, return_pointer)

        self.loaded_plugins[plugin_stub] = return_pointer.contents
