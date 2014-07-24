
import sys
import threading
import time
import traceback

import zmq

from madz.bootstrap import *
from ..IMinion import IMinion
from ..Daemon import Daemon

@bootstrap_plugin("madz.minion.Command")
class CommandMinion(IMinion):
    current = None

    class CommandThread(threading.Thread):
        def __init__(self, minion):
            super().__init__()
            self._minion = minion

        def run(self):
            context = zmq.Context()
            socket = context.socket(zmq.REP)
            socket.bind("tcp://127.0.0.1:{port}".format(port=self._minion.port))
            while not self._minion.banished:
                try:
                    command = socket.recv_pyobj(zmq.NOBLOCK)
                except zmq.ZMQError:
                    time.sleep(0.1)
                    continue
                report = None
                try:
                    #TODO: set up logging report
                    logger.info("DAEMON[{}] Doing command '{}'.".format(self._minion.minion_identity(), " ".join(command[0])))
                    execute_args_across(self._minion, command[0], Daemon.current.system, command[1])
                except Exception as e:
                    tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
                    logger.error("DAEMON[{}] Failed on command '{}':\n\t{}".format(self._minion.minion_identity(), " ".join(command[0]), tb_string))
                    pass #TODO: Create exception report, combine and send
                    report = tb_string
                socket.send_pyobj(report)

    def __init__(self):
        self.banished = False
        self.spawned = False
        self._thread = CommandMinion.CommandThread(self)
        self.port = Daemon.next_minion_port()

    @classmethod
    def minion_spawn(cls):
        if (cls.current is None):
            cls.current = CommandMinion()
        return cls.current._spawn()

    def _spawn(self):
        if not (self.spawned):
            self.spawned = True
            self._thread.start()
        return (self, [self.port])

    def minion_banish(self):
        self.banished = True
        self._thread.join()

    @classmethod
    def minion_identity(cls):
        return "command"
    
    @classmethod
    def minion_index(cls):
        return None

from ...config import *
from ...helper import logging_setup
from ...action import *
import argparse

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

def _plugin_names_from_file(file_path):
    """Given a file determine the full names of their plugins

    args:
        Files: list of string filenames

    returns:
        List of plugin names
    """
    file_path = file_path[0][0]

    def _find_nearest_plugin(path):
        while(path != os.getcwd()):
            head, tail = os.path.split(path)
            for d in os.listdir(head):
                if d.find("__plugin__.py") != -1:
                    return head + "/" + d
            path = head
        return ""

    if file_path.find("__plugin__.py") == -1:
        file_path = _find_nearest_plugin(file_path)

    if file_path == "":
        return ""

    else:
        imp = importlib.machinery.SourceFileLoader("__plugin__", file_path)
        plugin = imp.load_module("__plugin__")
        return plugin.plugin.name

def execute_args_across(minion, argv, system, user_config):
    """Executes the commands from a list of plugin configurations across a provided system from the command line.
    
    Args:
        argv: List of arguments from the command line
        system: A system object which the Configurations will be applied to
        user_config: A list of Configurations
    """
    # Apply system and user config.
    with config.and_merge(system.config):
        with config.and_merge(user_config):
            # Build valid command list for arg parsing
            # We can't build modes because that would require us to apply the command config.
            valid_commands = list(map(lambda c: c.label, config.get_option_type(CommandConfig)))

            # Parse the arguments
            args = generate_parser(valid_commands).parse_args(argv[1:])

            # Setup logging level
            if not (logging_setup._log_ch is None):
                logging_setup._log_ch.setLevel(logging_setup._log_level_name_index[args.log_level])

            system.index()

            if not (args.plugins_from_file == None):
                if args.plugins == None:
                    args.plugins = [[_plugin_names_from_file(args.plugins_from_file)]]
                else:
                    args.plugins += [_plugin_names_from_file(args.plugins_from_file)]

            # Setup active plugins
            if not (args.plugins is None):
                active_plugins = [item for sublist in args.plugins for item in sublist]
                system.set_active_plugins(system.resolve_plugins(active_plugins))

            # Expand out the parsed arguments
            parsed_commands = args.commands
            parsed_modes = args.modes

            # Apply Commands
            for parsed_command in parsed_commands:
                logger.debug("Starting command '{}'".format(parsed_command))
                with config.and_merge(config.get(CommandConfig.make_key(parsed_command))):
                    # Apply Modes
                    old_config_state = config.copy_state()
                    for parsed_mode in [item for sublist in parsed_modes for item in sublist]:
                        logger.debug("Entering mode '{}'".format(parsed_mode))
                        # TODO: Check for non-existent ModeConfigs
                        config.add(config.get(ModeConfig.make_key(parsed_mode)))

                    # Do Actions
                    for action in config.get(OptionCommandActions):
                        logger.debug("Starting action '{}'".format(action))
                        action = actions[action](system)
                        action.do(end_check = lambda m=minion: m.banished)
                        if minion.banished:
                            break

                    # Remove Modes, safely clean up config.
                    config.set_state(old_config_state)
