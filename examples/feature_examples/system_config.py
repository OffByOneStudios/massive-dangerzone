# This includes all configs and options relevent to system configuration.
# This can be included in the start script as well.
from madz.system_config import *

config = SystemConfig([
	# An example library config for the cmath library.
	LibraryConfig("math", [
		OptionLibraryStaticLinks("m")
	]),
])
