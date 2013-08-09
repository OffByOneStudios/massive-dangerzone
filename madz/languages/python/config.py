
from ..c.config import *

class Config(Config):
    def _default_options(self):
        return [
            OptionLibrarySearchPaths(),
            OptionLibraryStaticLinks(),
            OptionLibraryDynamicLinks(),
            OptionHeaderSearchPaths(),
            OptionHeaderIncludes(),
        ]

