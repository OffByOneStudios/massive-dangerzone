import sys
sys.path.append("../../")

# # # # # # LOGGING # # # #
import logging
# create console handler and set level to debug
log_ch = logging.StreamHandler()
log_ch.setLevel(logging.DEBUG)

# create formatter
log_formatter = logging.Formatter('%(asctime)-15s - %(levelname)s - %(name)-8s\n\t%(message)s')

# add formatter to ch
log_ch.setFormatter(log_formatter)

# add ch to logger
logging.getLogger("madz").setLevel(logging.DEBUG)
logging.getLogger("madz").addHandler(log_ch)
# # # # END LOGGING # # # #

import madz.system

test_plugin_system = madz.system.PluginSystem("madztests")
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

