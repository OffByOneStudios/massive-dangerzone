

import threading
import time

import zmq

from .IMinion import IMinion
from ..Daemon import Daemon

class ExecuterMinion(IMinion):
    current = []

    def __init__(self):
        self.current.append(self)

    @classmethod
    def spawn(cls):
        raise NotImplementedError()

    def banish(self):
        pass
        # OS kill?

    @classmethod
    def identity(cls):
        return "executer"

