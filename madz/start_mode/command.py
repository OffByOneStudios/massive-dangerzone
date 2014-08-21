"""madz/start_mode/command.py
@OffbyOne Studios 2014
Srtartmode for executing a build command across the plugin system.
"""

import argparse

from madz.config import *
from madz.bootstrap import *
import madz.start_mode.core as core

from madz.daemon.core.Client import Client

@bootstrap_plugin("madz.start_mode.command")
class CommandStartMode(core.IStartMode):
    def startmode_start(self, argv, system, user_config):
        with config.and_merge(system.config):
            with config.and_merge(user_config):
                # Build valid command list for arg parsing
                # We can't build modes because that would require us to apply the command config.
                valid_commands = list(map(lambda c: c.label, config.get_option_type(CommandConfig)))

                # Parse the arguments
                args = generate_parser(valid_commands).parse_args(argv[1:])

                kwargs = vars(args)
                kwargs["user_config"] = user_config
                res = Client().invoke_minion("command", kwargs)

                print(res)

    @classmethod
    def startmode_identity(self):
        return "command"



def generate_parser(valid_commands):
    """Creates a parser for actions on a plugin system.

    Args:
        valid_commands: A list of commands which are allowed to be performed on a plugin system.

    Returns:
        An argparse.ArgumentParser object
    """
    parser = argparse.ArgumentParser(description='Perform actions across a plugin system.')

    parser.add_argument("commands",
        action='store',
        nargs='+',
        choices=valid_commands,
        help="The command(s) to execute on the system, in order.")
    parser.add_argument("-m", "--modes",
        action='append',
        default=[],
        nargs='*',
        help="The modes to apply to the system before executing it.")
    parser.add_argument("-l", "--log-level",
        action='store',
        default="info",
        choices=["debug", "info", "warning", "error"],
        help="The log level to use for this execution.")
    parser.add_argument("-p", "--plugins",
        action='append',
        default=None,
        nargs='*',
        help="The plugins to perform the action on, not recommended for some actions.")
    parser.add_argument("--plugins-from-file",
        action='append',
        default=None,
        nargs='*',
        help="A file who's associated plugin actions are to be performed on"
        )

    def exit(self, status=0, message=None): raise Exception("Argparse Exit!:\n" + str(message))
    def error(self, message=None): raise Exception("Argparse Error!\n" + str(message))

    parser.exit = exit
    parser.error = error

    return parser
