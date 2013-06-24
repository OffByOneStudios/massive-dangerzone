import os, sys
import subprocess

import shared

class Builder(object):
    lang = shared.LanguageShared

    def __init__(self, plugin_stub):
        self.plugin_stub = plugin_stub
        self._s_dir = self.plugin_stub.abs_directory
        self._b_dir = self.lang.get_build_directory(self.plugin_stub)
        self._w_dir = self.lang.get_wrap_directory(self.plugin_stub)
        self._o_dir = self.lang.get_output_directory(self.plugin_stub)

    def prep(self):
        if not (os.path.exists(self._b_dir)):
            os.makedirs(self._b_dir)

        if not (os.path.exists(self._o_dir)):
            os.makedirs(self._o_dir)

    def build(self):
        self.prep()

        compile_files = []
        for f in os.listdir(self._s_dir):
            if os.path.isfile(os.path.join(self._s_dir, f)) and f.endswith(".c"):
                compile_files.append(os.path.join("..", f))
        compile_files.append(self.lang.get_c_code_filename(self.plugin_stub))

        obj_compile = subprocess.Popen(
            ["gcc", "-c", "-I"+self._w_dir, "-fpic"] + compile_files,
            cwd=self._b_dir,
            stdout=subprocess.PIPE)
        print "*** => COMPILE"
        print obj_compile.stdout.read()

        object_files = map(lambda c: os.path.basename(c)[:-2] + ".o", compile_files)

        out_link = subprocess.Popen(
            ["gcc", "-shared", "-o", os.path.join(self._o_dir, self.plugin_stub.id.namespace + ".madz")] + object_files,
            cwd=self._b_dir,
            stdout=subprocess.PIPE)
        print "*** => LINK"
        print out_link.stdout.read()

