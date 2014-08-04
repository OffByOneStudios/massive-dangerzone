"""madzmodule:start_mode/new/NewStartMode.py
@OffbyOne Studios 2014
Startmode for creating new plugins
"""
import os
import argparse

from madz.bootstrap import *
from madz.daemon.core.Client import Client

from madzmodule.start_mode.core.IStartMode import IStartMode

@bootstrap_plugin("madzmodule.start_mode.new")
class NewStartMode(IStartMode):
    """Class which starts a minion to create a new plugin"""

    def __init__(self):
        self._argparser = None

    @classmethod
    def add_argparser(self, subparser):
        """Argparser for this module sub-startmode"""
        self._argparser = subparser.add_parser(NewStartMode.startmode_identity(), description='Create new plugin')
        self._argparser.add_argument("namespace", help="Namespace of module")
        self._argparser.add_argument("language", help="Language of module")
        self._argparser.add_argument("path", action=AbsolutePathAction, help="Root of module hierarchy for new module")
        self._argparser.add_argument("-a", "--author", default="Someone's PC", help="Author of module")
        self._argparser.add_argument("-n", "--name", help="Module implementation name (defaults to language)")
        self._argparser.add_argument("-v", "--version", default="0.1.0", help="Module version")
        self._argparser.add_argument("-m", "--mdl-name", help="Name of Mdl file to generate. Defaults to namespace tail")
        self._argparser.add_argument("-d", "--depends", default=[], nargs="+", help="Dependent modules")
        self._argparser.add_argument("-i", "--imports", default=[], nargs="+", help="Imported modules")
        self._argparser.add_argument("-f", "--force", const=True, nargs="?", default=False, help="Overwrite module files where names conflict")
    def startmode_start(self, parsed_args):
        """Start this module sub-startmode

        Args:
            the result of calling parse on the argparser retrived from this class
        """

        args = vars(parsed_args)

        # Clean up some defaults
        args["name"] = args.get("name", args["language"])
        args["mdl-name"] = args.get("mdl-name", "{}.mdl".format(args["namespace"].split(".")[-1]))


        res = Client().invoke_minion("module",  vars(parsed_args))



    @classmethod
    def startmode_identity(self):
        return "new"


class AbsolutePathAction(argparse.Action):

    def __init__(self, **kwargs):
        argparse.Action.__init__(self, **kwargs)


    def __call__(self, parser, namespace, values, option_string):
        setattr(namespace, "path", os.path.abspath(values))

