import os, sys
import subprocess

class Builder(object):
    def __init__(self, plugin_stub):
        self.plugin_stub = plugin_stub

    def get_wrap_directory(self):
        return os.path.join("..", ".wrap-c")

    def get_build_directory(self):
        return os.path.join(self.plugin_stub.directory, ".build-c")

    def get_output_directory(self):
        return os.path.join(self.plugin_stub.directory, ".output")

    def prep(self):
        b_dir = self.get_build_directory()
        if not (os.path.exists(b_dir)):
            os.makedirs(b_dir)

        o_dir = self.get_output_directory()
        if not (os.path.exists(o_dir)):
            os.makedirs(o_dir)

    def build(self):
        self.prep()

        s_dir = self.plugin_stub.directory
        b_dir = self.get_build_directory()
        o_dir = self.get_output_directory()
        compile_files = []
        for f in os.listdir(s_dir):
            if os.path.isfile(os.path.join(s_dir, f)) and f.endswith(".c"):
                compile_files.append(os.path.join("..", f))

        print compile_files

        print "-I"+self.get_wrap_directory()
        subprocess.Popen(["gcc", "-c", "-I"+self.get_wrap_directory(), "-fpic"] + compile_files, cwd=b_dir)

        object_files = map(lambda c: os.path.basename(c)[:-2] + ".o", compile_files)

        subprocess.Popen(["gcc", "-shared", "-o", os.path.join(o_dir, self.plugin_stub.id.namespace + ".madz")] + object_files, cwd=b_dir)

