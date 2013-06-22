import sys
sys.path.append("../../")

import madz.system

test_plugin_system = madz.system.PluginSystem("madztests")
test_plugin_system.load_plugin_directory("plugins")

test_plugin_system.init_plugins()

for p in test_plugin_system.plugin_stubs:
    print "{} in '{}' with dependencies: {}".format(p.id, p.language, p.gen_recursive_loaded_depends())

p_a = test_plugin_system.get_plugin("a")

import madz.wrapper

test_wrap_gen = madz.wrapper.WrapperSystem(test_plugin_system)
test_wrap_gen.wrap()

import madz.builder

test_builder = madz.builder.BuilderSystem(test_plugin_system)
test_builder.build_plugin(p_a)

import madz.loader

test_loader = madz.loader.LoaderSystem(test_plugin_system)
test_loader.load_plugin(p_a)

