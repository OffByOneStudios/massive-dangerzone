
import sys
import os
import threading
import time
import subprocess
import logging

logger = logging.getLogger(__name__)

import zmq

from .IMinion import IMinion
from ..Daemon import Daemon

class ExecuterMinion(IMinion):
    current = []

    def __init__(self):
        self.current.append(self)

        self.port = Daemon.next_minion_port()
        self._bind_str = "tcp://127.0.0.1:{port}".format(port=self.port)
        self._proc_bootstrapper = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    def execute(self, dir=None):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.bind(self._bind_str)

        subproc = subprocess.Popen(
            [sys.executable, self._proc_bootstrapper, self._bind_str],
            cwd=os.path.dirname(self._proc_bootstrapper) if dir is None else dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    @staticmethod
    def _gen_load_pattern(plugin_stub, until="final"):
        # base:
        res = []

        # get into memory:
        res += [("in-mem", plugin_stub, [])]
        if until == "in-mem":
            return res

        # init:
        depends = plugin_stub.gen_recursive_loaded_depends()
        res += [load_pattern for require in depends for load_pattern in ExecuterMinion._gen_load_pattern(require, "inited")]
        res += [("inited", plugin_stub, depends)]
        if until == "inited":
            return res

        # final
        imports = list(filter(lambda p: p not in depends, plugin_stub.gen_required_loaded_imports()))
        res += [load_pattern for require in imports for load_pattern in ExecuterMinion._gen_load_pattern(require, "final")]
        res += [("final", plugin_stub, imports)]
        if until == "final":
            return res

    def load(plugin_stub):
        for p in ExecuterMinion._gen_load_pattern(plugin_strub):
            # Cleanup object for sending:
            load_type, plugin_stub, requires = p
            sending = (
                "load", 
                load_type, 
                plugin_stub.output_file_location(), 
                list(map(lambda p: p.output_file_location(), requires)))

            self.socket.send_pyobj(p)
            res = self.socket.recv_pyobj()

            # Executer responded with traceback
            if (isinstance(res, str)):
                logger.error("DAEMON[{}] Encountered problem loading {}:\n\t{}".format(self.identity(), plugin_stub, res))
                raise Exception("Encountered problem loading {}!".format(plugin_stub))

    def call_func(plugin_stub, func):
        index = plugin_stub.get_function_index(func)
        self.socket.send_pyobj(("execute", plugin_stub.output_file_location(), index))

        self.socket.close()
        self.context.term()

    @classmethod
    def spawn(cls):
        raise NotImplementedError()

    def banish(self):
        pass
        # OS kill?

    @classmethod
    def identity(cls):
        return "executer"

