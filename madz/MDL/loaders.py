import os
import pickle
import logging
from abc import *

from .parser_impl import generate_parser, get_result

MDLparser = generate_parser()

logger = logging.getLogger(__name__)

class IMdlLoader(metaclass=ABCMeta):
    @abstractmethod
    def load(self, dir=""):
        pass

    def dependency_files(self, dir=""):
        return []
        
class IMdlPickleable(IMdlLoader):
    @abstractmethod
    def source(self, dir="."):
        pass
        
          
class MdlRawLoader(IMdlLoader):
    
    def __init__(self, nodes):
        self.nodes = nodes

    def load(self, dir=""):
        return self.nodes
        

class MdlStringLoader(IMdlPickleable):

    def __init__(self, string):
        self.string = string
        
    def load(self, dir=""):
        return get_result(MDLparser.parse(self.string))
    
    def source(self, dir=""):
        return self.string
  
  
class MdlFileLoader(IMdlPickleable):
    
    def __init__(self, handle):
        self.handle = handle

    def _file(self, dir):
        return os.path.join(dir, self.handle)

    def dependency_files(self, dir=""):
        return [self._file(dir)]

    def load(self, dir="."):
        with open(self._file(dir)) as f:
            self.loader = MDLStringLoader(f.read())
            return self.loader.load()

    def source(self, dir="."):
        with open(self._file(dir)) as f:
            return f.read()
    
    
class MdlCachedLoader(IMdlLoader):

    def __init__(self, loader):
        self.loader = loader

    def _file(self, dir):
        return os.path.join(dir, ".madz")
        
    def load(self, dir=""):
        return self._parse_cached(self.loader.source(dir), dir)

    def dependency_files(self, dir=""):
        return [os.path.join(self._file(dir), "ast.pickle")]

    def _parse_cached(self, ast, dir):
        # Calculate directory of cache
        the_dir = self._file(dir)

        # Set state flag
        needs_parsing = True
        # Check for cache pickle file
        if os.path.exists(the_dir) and "ast.pickle" in os.listdir(the_dir):
            # Open cache file
            pickle_file = open(os.path.join(the_dir, "ast.pickle"), "rb")

            # Unpickle original source
            ast_str = pickle.load(pickle_file)
            # Check that the current source and original source match
            if ast_str == ast:
                logger.debug("Loading MDL...")
                needs_parsing = False

                # Unpack cached AST
                ast = pickle.load(pickle_file)
                # Close the file
                pickle_file.close()

        # Parse AST syntax
        if needs_parsing:
            logger.debug("Parsing MDL...")
            # Make the directory for the cache file
            if not os.path.exists(the_dir):
                os.mkdir(the_dir)

            # Open the cache file
            pickle_file = open(os.path.join(the_dir, "ast.pickle"), "wb")
            # Save the original AST
            ast_str = ast

            #Parse
            try:
                ast = get_result(MDLparser.parse(ast))
            except Exception as e:
                # Write bad parse and rethrow
                pickle.dump("", pickle_file)
                pickle.dump([], pickle_file)
                pickle_file.close()
                raise e
            # Write successful parse
            pickle.dump(ast_str, pickle_file)
            pickle.dump(ast, pickle_file)
            pickle_file.close()

        return ast
        