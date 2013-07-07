# Add null logging handler
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.getLogger(__name__).setLevel(logging.DEBUG)

_logging_default_formatter = logging.Formatter('%(asctime)-15s - %(levelname)s - %(name)-8s\n\t%(message)s')

def logging_add_console(level=logging.DEBUG, formatter=_logging_default_formatter):
    # create stream handler
    log_ch = logging.StreamHandler()

    # set stream handler level
    log_ch.setLevel(level)

    # add formatter to ch
    log_ch.setFormatter(formatter)

    # add ch to logger
    logging.getLogger(__name__).addHandler(log_ch)


def logging_add_file(filename, mode="a", level=logging.DEBUG, formatter=_logging_default_formatter):
    # create stream handler
    log_fh = logging.FileHandler(filename, mode)

    # set stream handler level
    log_fh.setLevel(level)

    # add formatter to ch
    log_fh.setFormatter(formatter)

    # add ch to logger
    logging.getLogger(__name__).addHandler(log_fh)
