
class Loader(object):
    def __init__(self, language):
        self.language = language

    def pre_init(self, loader, ctypes_dll):
        pass

    def post_init(self, loader, ctypes_dll):
        pass

    def post_initimports(self, loader, ctypes_dll):
        pass
