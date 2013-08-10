#!/usr/bin/python3

#### A hack to bypass installing madz for this example
import os, sys
sys.path.append("../../")


#### This imports all of the symbols needed in start scripts, like this one
from madz.start_script import *


#### We setup logging first so we can catch config errors.
# Bind the logging system to standard out
logging.bind_to_standard_out()
# Bind the logging system to a file as well
logging.bind_to_file(os.path.join(os.path.dirname(__file__), "./example.log"))


#### Next we load the configuration information.
## Configurations can include everything from libraries, compiler, and 
## language setup to new commands, platform information, and plugin load order.
##
## * User configs represent machine and user specific config information.
## * System configs represent project specific config information.
## * Plugin configs represent per plugin config information (automatic).

# Load the user config, normally this would be using a project configurable
# environment variable. Here we hardcode it.
config.bind_user_config("MADZ_FEATURE_EXAMPLES_USER_CONFIG", hardcode="./user_config.py")

# Switch logging over to the config information it now has avalible from the
# user config.
logging.use_config()

# Load the system config, often in a seperate file due to it's size.
import system_config
our_system_config = system_config.config


#### Now we intialize the plugin system.

# This makes a system of plugins. While we will generally work on one system,
# it is theoretically possible to have more than one.
system = core.make_system(our_system_config)

# This adds two directories of plugins. See the index.txt file for a list of
# the plugins found in this example. The second directory actually represents
# a location deeper into the first directory.
system.add_directory(core.make_directory("./plugins/"))
system.add_directory(core.make_directory("./plugins_secondary/"), "multidir.overlap")

# This checks all of the plugins and loads their information. May take a bit.
system.index()

# This executes the system using the command line arguments and config
# information. This allows you to modify the command line arguments.
helper.execute_system(system, sys.argv)

# The plugin system is now running the command it was given.
