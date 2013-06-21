import sys
sys.path.append("../../madz")

import system

test_plugin_system = system.PluginSystem("madztests")
test_plugin_system.load_plugin_directory("plugins")

for p in test_plugin_system.plugin_descriptions.values():
    print "{} in '{}' with dependencies: {}".format(p.id, p.language, p.dependencies)
