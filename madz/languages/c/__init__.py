import from_inter
class WrapperGenerator(object):
    def __init__(self, plugin_stub):
        self.plugin_stub = plugin_stub

    def get_build_directory(self):
        return os.path.join(self.plugin_stub.directory, ".wrap-c")

    def prep(self):
        b_dir = self.get_build_directory()
        if not (os.path.exists(b_dir)):
            os.makedirs(b_dir)

    def generate(self):
        p = From_Inter()
        self.prep()
        b_dir = self.get_build_directory()

