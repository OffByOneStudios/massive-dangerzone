import madz
import logging
import sys

_logging_default_formatter = logging.Formatter('%(asctime)-15s - %(levelname)s - %(name)-8s\n\t%(message)s')

_log_level_name_index = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR
}

_log_ch = None

def bind_to_standard_out(level=logging.DEBUG, formatter=_logging_default_formatter, check_argv=sys.argv):
    """Binds output from the logging system to standard out.
    
    Args:
        level: The level of the logging system to bind to standard out
        formatter: The formatting style for messages sent to standard out
        check_argv: Arguments from the command line
    """
    def pre_check_logger_level(argv, default=logging.DEBUG):
        if "-l" in argv:
            loc = argv.index("-l")
        elif "--log-level" in argv:
            loc = argv.index("--log-level")
        else:
            return default

        value = argv[loc+1]

        return _log_level_name_index.get(value, default)

    if check_argv:
        level = pre_check_logger_level(check_argv, level)

    # create stream handler
    log_ch = logging.StreamHandler()

    # bind to global
    global _log_ch
    _log_ch = log_ch

    # set stream handler level
    log_ch.setLevel(level)

    # add formatter to ch
    log_ch.setFormatter(formatter)

    # add ch to logger
    logging.getLogger(madz.__name__).addHandler(log_ch)

_log_fh = None

def bind_to_file(filename, mode="a", level=logging.DEBUG, formatter=_logging_default_formatter):
    """Binds output from the logging system to a file
    
    Args:
        filename: String representing the name of the file to output logging
        mode: Mode for writing to file
        level: Logging level for output to file
        formatter: The formatting style for messages sent to standard out
    """
    # create stream handler
    log_fh = logging.FileHandler(filename, mode)

    # bind to global
    global _log_fh
    _log_fh = log_fh

    # set stream handler level
    log_fh.setLevel(level)

    # add formatter to ch
    log_fh.setFormatter(formatter)

    # add ch to logger
    logging.getLogger(madz.__name__).addHandler(log_fh)

def use_config():
    # TODO: new logging stuff, with logging config options
    pass

