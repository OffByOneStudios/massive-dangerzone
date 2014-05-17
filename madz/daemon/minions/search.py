
import sys
import threading
import time
import traceback

import zmq

from madz.bootstrap import *
from ...plugins import query_tools
from ..IMinion import IMinion
from ..Daemon import Daemon

@bootstrap_plugin("madz.minion.Search")
class SearchMinion(IMinion):
    current = None
    
    tables = [query_tools.query_db.MdlTypeTable(), query_tools.query_db.MdlVarTable()]
    queries = {
                "declarations" : query_tools.query_db.MdlTypeTableQueryManager(), 
                "definitions" : query_tools.query_db.MdlVarTableQueryManager()
              }

    class SearchThread(threading.Thread):
        def __init__(self, minion):
            super().__init__()
            Daemon.current.system.index()
            self._minion = minion
            self._database = query_tools.QueryDatabase(file="madz.db", system=Daemon.current.system, table_handlers=SearchMinion.tables)
            self._database.start()
            self._database.index()

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
                    #TODO: Do things here
                    logger.info("DAEMON[{}] Searching Table '{}'.".format(self._minion.identity(), " ".join(command[0])))
                    report = execute_args_across(command[0], self._database.connection)
                    #execute_args_across(command[0], Daemon.current.system, command[1])
                except Exception as e:
                    tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
                    logger.error("DAEMON[{}] Failed on command '{}':\n\t{}".format(self._minion.identity(), " ".join(command[0]), tb_string))
                    pass #TODO: Create exception report, combine and send
                    report = tb_string
                socket.send_pyobj(report)

    def __init__(self):
        self.banished = False
        self.spawned = False
        self._thread = SearchMinion.SearchThread(self)
        self.port = Daemon.next_minion_port()

    @classmethod
    def spawn(cls):
        if (cls.current is None):
            cls.current = SearchMinion()
        return cls.current._spawn()

    def _spawn(self):
        if not (self.spawned):
            self.spawned = True
            self._thread.start()
        return (self, [self.port])

    def banish(self):
        self.banished = True
        self._thread.join()

    @classmethod
    def identity(cls):
        return "search"

from ...config import *
from ...helper import logging_setup
from ...action import *
import argparse

def generate_parser(table_names):
    """Creates a parser for searches on a plugin system.
    
    Args:
        valid_commands: A list of commands which are allowed to be performed on a plugin system.
        
    Returns:
        An argparse.ArgumentParser object
    """
    parser = argparse.ArgumentParser(description='Perform actions across a plugin system.')

    parser.add_argument("type",
        action='store',
        nargs=1,
        choices=table_names,
        help="The Tables to retrieve.")
    #parser.add_argument("-m", "--matchmode",
    #    action='append',
    #    choices=["none", "likeleft", "likeright", "likeboth"],
    #    default="none",
    #    nargs='*',
    #    help="The search mode of the query indicating ")
    
        

    def exit(self, status=0, message=None): raise Exception("Argparse Exit!:\n" + str(message))
    def error(self, message=None): raise Exception("Argparse Error!\n" + str(message))

    parser.exit = exit
    parser.error = error

    return parser

def execute_args_across(argv, db_connection):
    """Executes the commands from a list of plugin configurations across a provided system from the command line.
    
    Args:
        argv: List of arguments from the command line
        system: A system object which the Configurations will be applied to
        user_config: A list of Configurations
    """
    # Apply system and user config.
    print(argv)
    args = generate_parser(list(SearchMinion.queries.keys())).parse_args(argv[1:])
    res=[]
    for arg in args.type:
        res += SearchMinion.queries[arg].query(connection=db_connection)
    return res
         
