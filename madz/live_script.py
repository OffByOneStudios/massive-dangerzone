"""start_script.py
@OffbyOneStudios 2013
An import for running Madz in live mode
"""
import os, sys, imp

# logging namespace
from .helper import logging_setup as logging
from . import start_script as madz
    
class Daemon(object):
    """Class which runs madz in live mode"""
    
    def __init__(self, **kwargs):
        """Default constructor
        kwargs:
        user_config_env : Environment variable containing user config,
        log_to_stdout : Bool True if log message should be printed to stdout. Defaults to false.
        logging_file : String file to log to,
        plugin_directories : list of string directory names which contain plugins,
        system_configs : list of string fileanmes which contain system configs,
        executable_directories : string directory of executable plugin
        executable_config : file containing config for executable plugin
        """
        self.args = kwargs
        self.system = None
    
    def configure(self):
        # Bind User Config
        
        # Configure Logging
        if self.args.get("log_to_stdout", False) == True:
            print("Binding Daemon Logging to Standard Out")
            madz.logging.bind_to_standard_out()

        logging_file = self.args.get("logging_file")
        if not logging_file is None:
            madz.logging.bind_to_file(logging_file)
        
        
        system_config = None
        # Build Config
        for config_path in self.args.get("plugin_configs", []):
            with open(config_path) as module_file:
                config_tmp = imp.load_module("config", module_file, config_path, ('.py', 'r', imp.PY_SOURCE))
                if system_config is None:
                    system_config = config_tmp.config
                else:
                    system_config = system_config.merge(config_tmp.config)
        
        # Build the System
        self.system = madz.core.make_system(system_config)
        
        # Add Plugin Directories
        for directory in self.args.get("plugin_directories", []):
            self.system.add_directory(madz.core.make_directory(directory))
        
    def start(self):
        madz.helper.execute_system(self.system, ["live_daemon.py", "daemon"])

class Client(object):
    """Helper Class for issuing commands to the madz daemon
    
    Public Members
    log_level : Log Level Verbosity
    executable : string directory of active executable
    
    
    Private Members  
    _log_levels = ["error", "warn", "info", "debug"]
    """


    def __init__(self, config_args):
        """Default construtor
        
        Arguments:
            config_args : Dictionary of configuration variables listed in Daemon
        """

        import madz.start_script as madz
        self.madz = madz
        self._log_level = "info"
        self._log_levels = ["error", "warn", "info", "debug"]
        self._executables = config_args.get("executable_directories", None)
        self._executable = None
        self.config_args = config_args

        user_config_env = self.config_args.get("user_config_env", None)
        if not user_config_env is None:
            madz.config.bind_user_config(user_config_env)
        user_config_file = self.config_args.get("user_config_file", None)
        if not user_config_file is None:
            madz.config.bind_user_config(user_config_file)
        
    @property
    def log_level(self):
        return self._log_level

    @property
    def executable(self):
        return self._executable


    def set_executable(self, executable):
        """Configure active executable plugin

        Arguments:
            exectuable : string executable directory, string in executable list
        """
        self._executable = executable

    def set_log_level(self, level):
        """Configure Log Verbosity
        
        Arguments:
            Level : string log level, one of ["error", "warn", "info", "debug"]
        """
        if not level in self._log_levels:
            raise AttributeError("Invalid Log Level, use {}".format(self._log_levels))

        self.log_level = level


    def _make_raw_command(self, command, namespace=None):
        """Build raw Listargs
        
        Arguments:
            command: string command to run, [init, clean, wrap, make, execute]
            namespace: string namespace to execute
        """
        args = ["main.py"]
        if self.executable != None:
            args.append(self.executable)

        if command in ['init', 'wrap', 'clean', 'make', 'execute']:
            args.append("command")
            
        args.extend([command, "-l{}".format(self.log_level)])

        if not namespace is None:
            args.extend(["-p", namespace])

        return list(args)

    def run_raw(self, args):
        """Send a raw query to Daemon

        Args:
            args : list of string arguments to send.
        """
        self.madz.helper.execute_system(None, args)

    def kill(self):
        self.madz.helper.execute_system(None, ["main.py", "kill"])
    def init(self, namespace=None):
        """Init namespace, or all plugins if namespace is None"""
        self.madz.helper.execute_system(None, self._make_raw_command("init", namespace))

    def wrap(self, namespace=None):
        """Wrap namespace, or all plugins if namespace is None"""
        self.madz.helper.execute_system(None, self._make_raw_command("wrap", namespace))

    def clean(self, namespace=None):
        """Clean namespace, or all plugins if namespace is None"""
        self.madz.helper.execute_system(None, self._make_raw_command("clean", namespace))

    def make(self, namespace=None):
        """Make namespace, or all plugins if namespace is None"""
        self.madz.helper.execute_system(None, self._make_raw_command("make", namespace))

    def execute(self, namespace=None):
        """Make namespace, or all plugins if namespace is None"""
        if len(self.config_args.get("executable_directories", [])) == 0:
            raise AttributeError("Madz Project contains no Executables.")

        self.madz.helper.execute_system(None, self._make_raw_command("execute", namespace))
        