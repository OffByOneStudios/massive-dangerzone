"""madzide:madz.start_mode.module.py
@OffbyOne Studios 2014
Minion for performing operations on modules
"""

import argparse
import os

from madz.bootstrap import *
import madz.start_mode.core as core

from madz.daemon.core.Client import Client

import madzmodule
import madzmodule.start_mode.core




@bootstrap_plugin("madz.start_mode.module")
class ModuleStartMode(core.IStartMode):

    def __init__(self):
        self._parser = argparse.ArgumentParser(description='Perform operations on modules')
        self._subparsers = self._parser.add_subparsers(dest="start_mode")

        for sub_mode in madzmodule.start_mode.core.all_startmodes():
            sub_mode.add_argparser(self._subparsers)

    def startmode_start(self, argv, system, user_config):
        args = self._parser.parse_args(argv[1:])
        start_mode = madzmodule.start_mode.core.get_startmode(args.start_mode)()
        start_mode.startmode_start(args)

    @classmethod
    def startmode_identity(self):
        return "module"
