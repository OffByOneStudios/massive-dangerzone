import sys
sys.path.append("../../")

import madz.system

test_plugin_system = madz.system.PluginSystem("madztests")
test_plugin_system.load_plugin_directory("plugins")

for p in test_plugin_system.plugin_stubs.values():
    print "{} in '{}' with dependencies: {}".format(p.id, p.language, p.dependencies)

print test_plugin_system.get_plugin("a")

import madz.wrappergenerator

test_wrap_gen = madz.wrappergenerator.SystemWrapperGenerator(test_plugin_system)
test_wrap_gen.generate_wrappers()
