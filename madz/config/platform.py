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

    def __init__(self, language_name, options):
        self.language_name = language_name

    def get_key(self):
        return (self.__class__, self.library_name)

    def _str_view(self):
        return "Language Config for '{}'".format(self.get_language_name)


#
# Options
#

import platform
import sys

class OptionPlatformProcessorFamily(BaseChooseOption):
    possible_values = ["i386", "x86_64"]

    @classmethod
    def get_default_value(cls):
        return platform.machine()

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

