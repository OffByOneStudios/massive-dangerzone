"""madzmodule:start_mode/new/NewStartMode.py
@OffbyOne Studios 2014
Startmode for creating new plugins
"""
import os
import argparse

from madz.bootstrap import *
from madz.daemon.core.Client import Client

from madzmodule.start_mode.core.IStartMode import IStartMode

@bootstrap_plugin("madzmodule.start_mode.copy")
class CopyStartMode(IStartMode):
    """Class which starts a minion to create a new plugin"""

    def __init__(self):
        self._argparser = None

    @classmethod
    def add_argparser(self, subparser):
        """Argparser for this module sub-startmode"""
        self._argparser = subparser.add_parser(CopyStartMode.startmode_identity(), description='Create new plugin')
        self._argparser.add_argument("template", help="Namespace to copy")
        self._argparser.add_argument("namespace", help="Outgoing namespace")
        self._argparser.add_argument("path", action=AbsolutePathAction, help="Root of module hierarchy for new module")
        self._argparser.add_argument("-f", "--force", const=True, nargs="?", default=False, help="Overwrite module files where names conflict")

    def startmode_start(self, parsed_args):
        """Start this module sub-startmode

        Args:
            the result of calling parse on the argparser retrived from this class
        """

        args = vars(parsed_args)
        res = Client().invoke_minion("module",  vars(parsed_args))

    @classmethod
    def startmode_identity(self):
        return "copy"


class AbsolutePathAction(argparse.Action):

    def __init__(self, **kwargs):
        argparse.Action.__init__(self, **kwargs)


    def __call__(self, parser, namespace, values, option_string):
        setattr(namespace, "path", os.path.abspath(values))

