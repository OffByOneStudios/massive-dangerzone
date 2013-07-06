import importlib

class LanguageError(Exception): pass
class LanguageDoesNotExistError(LanguageError): pass

def get_language(language):
    #try:
    language_module = importlib.import_module("." + language, __name__)
    #except ImportError:
    # TODO(Mason) log import errors for debugging purposes
    #    raise LanguageDoesNotExistError("Language does not exist: '{}'".format(language))
    
    return language_module

