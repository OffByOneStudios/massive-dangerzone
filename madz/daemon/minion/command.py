"""madz/daemon/minion/command.py
@OffbyOne Studios 2014
Depreciated Command minion.
"""

import sys
import threading
import time
import traceback

import zmq

import pyext

from madz.bootstrap import *
from madz.daemon.minion.core import IMinion
from madz.daemon.core import Daemon

@bootstrap_plugin("madz.daemon.minion.command")
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
                command = pyext.zmq_busy(lambda: socket.recv_pyobj(zmq.NOBLOCK),
                    socket_end=lambda s=self: s._minion.banished)

                report = None
                try:
                    #TODO: set up logging report
                    logger.info("DAEMON[{}] Doing command '{}'.".format(self._minion.minion_identity(), " ".join(command["commands"])))
                    execute_args_across(self._minion, **command)
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

def execute_args_across(minion, **kwargs):
    """Executes the commands from a list of plugin configurations across a provided system from the command line.

    Args:
        kwargs: dict containing parsed arguments, user config, system config, etc.
    """
    # Setup logging level
    if not (logging_setup._log_ch is None):
      logging_setup._log_ch.setLevel(logging_setup._log_level_name_index[kwargs["log_level"]])

    Daemon.current.system.index()

    if not (kwargs["plugins_from_file"] == None):
        if kwargs["plugins"] == None:
            kwargs["plugins"] = [[_plugin_names_from_file(kwargs["plugins_from_file"])]]
        else:
            kwargs["plugins"] += [_plugin_names_from_file(kwargs["plugins_from_file"])]

    # Setup active plugins
    if not (kwargs["plugins"] is None):
        active_plugins = [item for sublist in kwargs["plugins"] for item in sublist]
        Daemon.current.system.set_active_plugins(kDaemon.current.system.resolve_plugins(active_plugins))

    # Expand out the parsed arguments
    parsed_commands = kwargs["commands"]
    parsed_modes = kwargs["modes"]

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
                action = actions[action](Daemon.current.system)
                action.do(end_check = lambda m=minion: m.banished)
                if minion.banished:
                   break

            # Remove Modes, safely clean up config.
            config.set_state(old_config_state)
