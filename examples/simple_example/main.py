import sys
sys.path.append("../../madz")

import system

test_plugin_system = system.PluginSystem("madztests")
test_plugin_system.load_plugin_directory("plugins")

import generator

test_plugin_generator = generator.Generator(test_plugin_system)
test_plugin_generator.gen_plugin
