from madz.languages.c import compiler_gcc as c_gcc


class GCCCompiler(c_gcc.GCCCompiler):
    #return ["gcc", "-I"+shared.LanguageShared.get_wrap_directory(self.plugin_stub) + "-IC:\Python33\include -LC:\Python33\libs", "-fpic"]
    pass