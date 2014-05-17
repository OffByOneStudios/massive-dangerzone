import os
import abc
import logging
import threading
import time
import signal

import zmq
import pydynecs

from .. import bootstrap
from . import *

logger = logging.getLogger(__name__)

daemon_filename = ".madz-daemon"

class Daemon(object):
    current = None

    def __init__(self, system):
        if not (Daemon.current is None):
            raise Exception("Can't re-init daemon.")
        Daemon.current = self

        self.context = zmq.Context()
        self.system = system
        self.minions = []
        self._ohshit = False

    @classmethod
    def next_minion_port(cls):
        cls.port += 1
        return cls.port

    def _sigint_handler(self, signum, frame):
        if (self._ohshit == True):
            exit(1)
        self._ohshit = True
        logger.critical("DAEMON[^]: Recieved SIGINT, shutting down now!")
        self.banish_minions()
        logger.critical("DAEMON[^]: Minions banished, one moment...")
        self.banish_daemon()
        logger.critical("DAEMON[^]: Daemon banished, have a nice day!")

    def spawn_minion(self, minion_class):
        minion, report = minion_class.spawn()
        self.minions.append(minion)
        return (minion, report)

    def describe_minions(self):
        return list(map(str, self.minions))

    def banish_minions(self):
        res = []
        for minion in self.minions:
            res += [minion.banish()]
        return res
        
    def banish_daemon(self):
        self._banished = True
        return []
        
    def start(self, **kwargs):
        try:
            Daemon.port = int(kwargs.get("port", 16239))
            force = bool(kwargs.get("force", False))
        except Exception as e:
            raise Exception("Failed to parse arguments.") from e

        try:
            if (not force) and os.path.exists(daemon_filename):
                raise Exception("Daemon file already exists, may need to delete.")
            with open(daemon_filename, "w") as f:
                f.write(str(Daemon.port))
        except Exception as e:
            raise Exception("Failed to write daemon file.") from e

        # overriding signal:
        _old_sig = signal.signal(signal.SIGINT, self._sigint_handler)

        self.control_socket = self.context.socket(zmq.REP)
        bind_str = "tcp://127.0.0.1:{port}".format(port=Daemon.port)
        self.control_socket.bind(bind_str)
        logger.info("DAEMON[^]: Started and bound to {}.".format(bind_str))

        self._banished = False

        try:
            while not self._banished:
                try:
                    invocation = self.control_socket.recv_multipart(zmq.NOBLOCK)
                except zmq.ZMQError:
                    try:
                        time.sleep(0.1)
                    except InterruptedError:
                        pass
                    continue
                invocation_command = invocation[0].decode("utf-8")

                if invocation_command == "identity-concepts":
                    logger.debug("DAEMON[^]: Listing identity concepts.")
                    result = [
                        "python-raw[0.4.0]".encode("utf-8"),
                    ]
                    self.control_socket.send_multipart(result)

                elif invocation_command == "minion":
                    minion_name = invocation[1].decode("utf-8")
                    logger.info("DAEMON[^]: Spawning minion {}.".format(minion_name))
                    if not (minion_name in bootstrap.EcsBootstrap[Minion.identity]):
                        self.control_socket.send_pyobj("Minion not found!")
                        continue
                    minion_plugin = bootstrap.EcsBootstrap[Minion.identity][minion_name]
                    minion_report = self.spawn_minion(minion_plugin[Minion])[1]
                    self.control_socket.send_pyobj(minion_report)

                elif invocation_command == "describe-minions":
                    logger.debug("DAEMON[^]: Describing minions.")
                    minion_report = self.describe_minions()
                    self.control_socket.send_pyobj(minion_report)

                elif invocation_command == "banish":
                    logger.info("DAEMON[^]: Banishing!")
                    banish_report = self.banish_minions()
                    banish_report += self.banish_daemon()
                    self.control_socket.send_pyobj(banish_report)
        finally:
            if os.path.exists(daemon_filename):
                os.remove(daemon_filename)
            self.control_socket.close()
            self.context.term()

            # fixing signal:
            signal.signal(signal.SIGINT, _old_sig)

