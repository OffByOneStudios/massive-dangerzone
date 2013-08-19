"""config/platform.py
@OffbyOne Studios 2013
Manages the configuration for platforms (meant for both current and target).
"""
from .base import *

#
# Config
#

class PlatformConfig(BaseConfig):
    """This represents the configuration for a platform.

    The make_default function for this class should ALWAYS be used as the current platform information.

    """
    platform_option_types=[]

    @classmethod
    def add_platform_option_type(cls, option_type):
        cls.platform_option_types.append(option_type)

    @classmethod
    def get_default_options(cls):
        return list(map(lambda o: o.make_default(), cls.platform_option_types))


#
# Options
#

import platform
import sys
import os

class OptionPlatformProcessorFamily(BaseChooseOption):
    possible_values = ["i386", "x86_64"]

    @classmethod
    def get_default_value(cls):
        return platform.machine()
PlatformConfig.add_platform_option_type(OptionPlatformProcessorFamily)

class OptionPlatformOperatingSystem(BaseChooseOption):
    possible_values = ["windows", "unix", "osx"]

    def is_posix(self):
        return value == "osx" or self.value == "unix"

    @classmethod
    def get_default_value(cls):
        if sys.platform =="darwin":
            return "osx"
        elif os.name == "nt":
            return "windows"
        elif os.name == "posix" or os.name == "mac":
            return "unix"
PlatformConfig.add_platform_option_type(OptionPlatformOperatingSystem)

#
# platform_check helpers
#

from .current import *

def PlatformCheckSkip(target_platform):
    return False

def PlatformCheckWindows(target_platform):
    return target_platform.get(OptionPlatformOperatingSystem) == "windows"

def PlatformCheckOSX(target_platform):
    return target_platform.get(OptionPlatformOperatingSystem) == "osx"

def PlatformCheckUnix(target_platform):
    return target_platform.get(OptionPlatformOperatingSystem) == "unix"