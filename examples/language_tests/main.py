import os, sys
sys.path.append("../../")

import madz

madz.logging_add_console()
madz.logging_add_file(os.path.join(os.path.dirname(__file__), "madz_test.log"))

import madz.system

name_filter = madz.system.NamespaceFilter("madz.languages.c.build", reverse=True)
test_plugin_system = madz.system.PluginSystem("madztests")
test_plugin_system.plugin_resolver.add_filter(name_filter)
test_plugin_system.load_plugin_directory("plugins")



test_plugin_system.init_plugins()

import madz.wrapper

test_wrap_gen = madz.wrapper.WrapperSystem(test_plugin_system)
test_wrap_gen.wrap()

import madz.builder

test_builder = madz.builder.BuilderSystem(test_plugin_system)
test_builder.build()

import madz.loader

test_loader = madz.loader.LoaderSystem(test_plugin_system)
test_loader.load()

import ctypes

ctest_plugin = test_plugin_system.get_plugin("tester")
func = test_loader.get_function(ctest_plugin, "test")
ctypes.CFUNCTYPE(None)(func)()

if len(sys.argv) > 1 and sys.argv[1] == "clean":
    import madz.cleaner

    test_cleaner = madz.cleaner.CleanerSystem(test_plugin_system)
    test_cleaner.clean()
