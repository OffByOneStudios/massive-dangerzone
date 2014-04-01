import os
import abc
import logging
import threading
import time

import zmq

logger = logging.getLogger(__name__)

daemon_filename = ".madz-daemon"

class Daemon(object):
    current = None

    handlers = {}

    def __init__(self, system):
        if not (Daemon.current is None):
            raise Exception("Can't re-init daemon.")
        Daemon.current = self

        self.context = zmq.Context()
        self.system = system
        self.minions = []

    @classmethod
    def next_minion_port(cls):
        cls.port += 1
        return cls.port

    def spawn_minion(self, minion_class):
        minion, report = minion_class.spawn()
        self.minions.append(minion)
        return report

    def describe_minions(self):
        return list(map(str, self.minions))

    def banish_minions(self):
        res = []
        for minion in self.minions:
            res += [minion.banish()]
        return res
        
    def banish_daemon(self):
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

        self.control_socket = self.context.socket(zmq.REP)
        bind_str = "tcp://127.0.0.1:{port}".format(port=Daemon.port)
        self.control_socket.bind(bind_str)
        logger.info("DAEMON[^]: Started and bound to {}.".format(bind_str))

        banished = False

        try:
            while not banished:
                try:
                    invocation = self.control_socket.recv_multipart()
                except ZMQError:
                    time.sleep(0.1)
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
                    minion_report = self.spawn_minion(raw_handlers[minion_name])
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
                    banished = True
        finally:
            if os.path.exists(daemon_filename):
                os.remove(daemon_filename)
            self.control_socket.close()
            self.context.term()

from .minions import *
