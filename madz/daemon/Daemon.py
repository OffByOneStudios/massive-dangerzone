"""daemon/Daemon.py
@OffbyOne Studios 2014
Contains the daemon manager, responsible for minions.
"""
import os
import abc
import logging
import threading
import traceback
import sys
import time
import signal

import zmq
import pyext
import pydynecs

from .. import bootstrap
from . import *

logger = logging.getLogger(__name__)

# Use better binding: http://stackoverflow.com/questions/16699890/connect-to-first-free-port-with-tcp-using-0mq
class Daemon(object):
    current = None

    def __init__(self, system):
        if not (Daemon.current is None):
            raise Exception("Can't re-init daemon.")
        Daemon.current = self

        self.context = zmq.Context()
        self.system = system
        self.minions = {}
        self._ohshit = False

    @classmethod
    def next_minion_port(cls):
        cls.port += 1
        return cls.port

    def _sigint_handler(self, signum, frame):
        if (self._ohshit == True):
            exit(1) # Fuckit, die die die
        self._ohshit = True
        logger.critical("DAEMON[^]: Recieved SIGINT, shutting down now!")
        self.banish_minions()
        logger.critical("DAEMON[^]: Minions banished, one moment...")
        self.banish_daemon()
        logger.critical("DAEMON[^]: Daemon banished, have a nice day!")
        exit(0)

    def spawn_minion(self, plugin):
        minion, report = plugin[Minion].minion_spawn()
        i = minion.minion_identity()
        
        if not i in self.minions:
            self.minions[i] = set()
        self.minions[i].add(minion)
        
        return (minion, report)

    def describe_minions(self):
        res = []
        for minion_t in self.minions.values():
            for minion in minion_t:
                res += [str(minion)]
        return res

    def banish_minion_type(self, name):
        res = []
        for minion in self.minions[name]:
            res.append(minion.minion_banish())
        del self.minions[name]
        return res
        
    def banish_minions(self):
        res = []
        for minion_name in list(self.minions.keys()):
            res += self.banish_minion_type(minion_name)
        return res
        
    def banish_daemon(self):
        self._banished = True
        return []
    
    invoke = pyext.multimethod(pyext.ArgMatchStrategy(True))
    
    @invoke.method()
    def invoke_error(self, cmd, *invoke):
        logger.error("DAEMON[^]: Bad invocation '{}'".format(cmd))
        self.control_socket.send_pyobj(None)
        
    @invoke.method("identity-concepts")
    def invoke_identity_concepts(self, cmd, *invoke):
        logger.debug("DAEMON[^]: Listing identity concepts.")
        result = [
            "python-raw[0.4.0]".encode("utf-8"),
        ]
        
        self.control_socket.send_pyobj(result)
    
    @invoke.method("minion")
    def invoke_minion(self, cmd, minion_name, *invoke):
        minion_name = minion_name.decode("utf-8")
        
        logger.info("DAEMON[^]: Spawning minion {}.".format(minion_name))
        if not (minion_name in bootstrap.EcsBootstrap.current[Minion_identity]):
            self.control_socket.send_pyobj("Minion not found!")
            return
        
        minion_plugin = bootstrap.EcsBootstrap.current[Minion_identity][minion_name]
        minion_report = self.spawn_minion(minion_plugin)[1]
        
        self.control_socket.send_pyobj(minion_report)
    
    @invoke.method("describe-minions")
    def invoke_describe_minions(self, cmd, *invoke):
        logger.debug("DAEMON[^]: Describing minions.")
        minion_report = self.describe_minions()
        
        self.control_socket.send_pyobj(minion_report)
    
    @invoke.method("banish-minion")
    def invoke_banish_minion(self, cmd, minion_name, *invoke):
        minion_name = minion_name.decode("utf-8")
        logger.debug("DAEMON[^]: Banishing minion '{}'.".format(minion_name))
        
        minion_report = self.banish_minion_type(minion_name)
        
        self.control_socket.send_pyobj(None)
                    
    @invoke.method("banish")
    def invoke_banish(self, cmd, *invoke):
        logger.info("DAEMON[^]: Banishing!")
        banish_report = self.banish_minions()
        banish_report += self.banish_daemon()
        
        self.control_socket.send_pyobj(banish_report)
    
    
    def start(self, **kwargs):
        try:
            Daemon.port = kwargs.get("port", None)
            force = bool(kwargs.get("force", False))
        except Exception as e:
            raise Exception("Failed to parse arguments.") from e

        if (not force) and os.path.exists(daemon_filename):
            raise Exception("Daemon file already exists, may need to delete.")

        # overriding signal:
        _old_sig = signal.signal(signal.SIGINT, self._sigint_handler)

        self.control_socket = self.context.socket(zmq.REP)
        
        Daemon.binding = pyext.ZmqBind(port=Daemon.port or "*")
        
        Daemon.binding.bind(self.control_socket)
        Daemon.port = int(Daemon.binding.port)
        
        logger.info("DAEMON[^]: Started and bound to {}.".format(Daemon.binding))

        try:
            with open(daemon_filename, "w") as f:
                f.write(str(Daemon.port))
        except Exception as e:
            raise Exception("Failed to write daemon file.") from e
        
        self._banished = False

        try:
            while not self._banished:
                invocation = pyext.zmq_busy(lambda: self.control_socket.recv_multipart(zmq.NOBLOCK), lambda: self._banished)
                try:
                    invocation_command = invocation[0].decode("utf-8")
                    
                    self.invoke(self, invocation_command, *invocation[1:])
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                    logger.error("DAEMON[^]: Malformed invocation!\n{}".format(tb))
                    self.control_socket.send_pyobj(None)

        finally:
            if os.path.exists(daemon_filename):
                os.remove(daemon_filename)
            self.control_socket.close()
            self.context.term()

            # fixing signal:
            signal.signal(signal.SIGINT, _old_sig)

