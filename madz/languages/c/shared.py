import os

class LanguageShared(object):
    @classmethod
    def get_wrap_directory(cls, plugin_stub):
        return os.path.join(plugin_stub.abs_directory, ".wrap-c")

    @classmethod
    def get_build_directory(cls, plugin_stub):
        return os.path.join(plugin_stub.abs_directory, ".build-c")

    @classmethod
    def get_output_directory(cls, plugin_stub):
        return os.path.join(plugin_stub.abs_directory, ".output")
