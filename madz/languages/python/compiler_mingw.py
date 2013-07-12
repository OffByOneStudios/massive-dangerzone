import madz.languages.c.compiler_mingw as c_mingw


class MinGWCompiler(c_mingw.MinGWCompiler):

    def args_compile(self, source_files):
    # print  [self.binary_name_compiler(), "-c", "-I"+self.language.get_wrap_directory(), "-IC:\Python33\include", "-LC:\Python33\libs"] + source_files  + ["-lpython33"]
        return [self.binary_name_compiler(), "-c", "-I"+self.language.get_wrap_directory(), "-IC:\Python33\include", "-LC:\Python33\libs"] + list(source_files)  + ["-lpython33"]


    def args_link(self, object_files):
        return [self.binary_name_linker(), "-shared", "-LC:\Python33\libs", "-o", self.language.get_output_file()] + list(object_files) + ["-lpython33"]

