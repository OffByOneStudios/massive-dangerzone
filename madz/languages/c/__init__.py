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

    hack = \
"""
#include<stdlib.h>
struct ___madz_TYPE_a * ___madz_this_output;
int ___madz_init(void * * dependencies, void * * requirements, void * * output) {
    ___madz_this_output = (struct ___madz_TYPE_a *)malloc(sizeof(___madz_TYPE_a));
    ___madz_this_output->distance = &___madz_output_distance;
    (*output) = ___madz_this_output;
}

"""

    def generate(self):
        self.prep()

        gen = from_inter.From_Inter()
        b_dir = self.get_build_directory()

        with open(os.path.join(b_dir, "madz.h"), "w") as f:
            f.write(gen.make_typedefs(self.plugin_stub))
            f.write(gen.make_structs(self.plugin_stub))
            f.write(self.hack)

import build

Builder = build.Builder
