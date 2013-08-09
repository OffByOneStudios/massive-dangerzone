
from ..config import *

class Config(LanguageConfig):
    def _default_options(self):
        return [
            OptionLibrarySearchPaths(),
            OptionLibraryStaticLinks(),
            OptionLibraryDynamicLinks(),
            OptionHeaderSearchPaths(),
            OptionHeaderIncludes(),
        ]

class OptionLibrarySearchPaths(BaseAppendOption): pass
class OptionLibraryStaticLinks(BaseAppendOption): pass
class OptionLibraryDynamicLinks(BaseAppendOption): pass
class OptionHeaderSearchPaths(BaseAppendOption): pass
class OptionHeaderIncludes(BaseAppendOption): pass
