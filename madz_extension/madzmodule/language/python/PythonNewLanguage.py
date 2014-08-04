"""madzmodule:module/new/language/python/PythonNewLanguage.py
@OffbyOne Studios 2014
Class for generating new Python files.
"""

from madz.bootstrap import *

from madzmodule.language.core import *

@bootstrap_plugin("madzmodule.language.python")
class PythonNewLanguage(INewLanguage):
    """Class for generating new python files"""

    def newlanguage_generate(self, **kwargs):
        """Perform this module operation."""
        return python_template.format(**kwargs)

    @classmethod
    def newlanguage_identity(self):
        return "python"

    @classmethod
    def newlanguage_extension(self):
        return "py"




python_template=\
"""#{namespace}.madz.py
# @{author} {date}
# A New Module

import madz

#Fill in Initialization Code Here.
"""
