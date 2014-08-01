"""ide:madz/start_mode/ide.py
@OffbyOne Studios 2014
Startmode for launching ide helper functionality.
"""

import argparse
import os

from madz.bootstrap import *
import madz.start_mode.core as core

from madz.daemon.core.Client import Client

import madzide

parser = argparse.ArgumentParser(description='Generate IDE project files.')
parser.add_argument('ide', help='IDE for which to generate files.')
parser.add_argument('output_directory', help='Directory in which to generate project files')

@bootstrap_plugin("madz.start_mode.ide")
class IDEStartMode(core.IStartMode):
    def startmode_start(self, argv, system, user_config):
        args=parser.parse_args(argv[1:])

        #unpack argparse
        kwargs= {
            "user_config" : user_config,
            "client_path" : os.path.abspath(os.path.join(os.getcwd(), argv[0])),
            "ide" : args.ide,
            "output_directory" : os.path.abspath(args.output_directory)
        }
        res = Client().invoke_minion("ide", kwargs)

    @classmethod
    def startmode_identity(self):
        return "ide"
