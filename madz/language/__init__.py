import os
import sys
import importlib
import traceback
import logging

logger = logging.getLogger(__name__)

class LanguageError(Exception): pass
class LanguageDoesNotExistError(LanguageError): pass

def get_language(language):
    """Retrieves a named language module from madz.
    
    Args:
        language: A string of the name of the language to retrieve.
        
    Returns:
        A Language Module
    """
    if not os.path.exists(os.path.join(os.path.dirname(__file__), language)):
         LanguageDoesNotExistError("Could not find folder for language: {}".format(language))

    try:
        language_module = importlib.import_module("." + language, __name__)
    except ImportError as exec:
        tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
        logger.error("Failed to load language '{}':\n\t{}".format(language, tb_string))
        raise LanguageError from exec

    return language_module

