import from_inter
import os

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
        self.prep()

        gen = from_inter.From_Inter()
        b_dir = self.get_build_directory()

        with open(os.path.join(b_dir, "madz.h"), "w") as f:
            f.write(gen.make_typedefs(self.plugin_stub))
            f.write(gen.make_structs(self.plugin_stub))

import build

Builder = build.Builder
