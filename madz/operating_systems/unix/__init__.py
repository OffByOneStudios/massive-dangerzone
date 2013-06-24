import ctypes
import os

class UnixOperatingSystem(object):
    def __init__(self):
        self.loaded_plugins = {}

    @staticmethod
    def output_file_location(plugin_stub):
        return os.path.join(plugin_stub.directory, ".output", plugin_stub.id.namespace + ".madz")

    def load(self, plugin_stub):
        plugin_dll = ctypes.cdll.LoadLibrary(self.output_file_location(plugin_stub))
        
        madz_init = getattr(plugin_dll, "___madz_EXTERN_INIT")
        madz_init.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p)]

        return_pointer = ctypes.pointer(ctypes.c_void_p())

        depends = plugin_stub.depends
        imports = plugin_stub.imports

        depends_array = (ctypes.c_void_p * len(depends))()
        imports_array = (ctypes.c_void_p * len(imports))()

        # TODO(Mason): assign values into arrays

        error_val = madz_init(depends_array, imports_array, return_pointer)

        self.loaded_plugins[plugin_stub] = return_pointer.contents

