"""madzmodule:module/new/language/c/CNewLanguage.py
@OffbyOne Studios 2014
Class for generating new C files.
"""

from madz.bootstrap import *

from madzmodule.language.core import *

@bootstrap_plugin("madzmodule.language.c")
class CNewLanguage(INewLanguage):
    """Class for generating new c files"""

    def newlanguage_generate(self, **kwargs):
        """Perform this module operation."""
        return c_template.format(**kwargs)

    @classmethod
    def newlanguage_identity(self):
        return "c"

    @classmethod
    def newlanguage_extension(self):
        return "c"




c_template=\
"""/*{namespace}.madz.c
* @{author} {date}
* A New Module
*/
#include ".madz/c/.wrap-c/madz.h"

MADZINIT{{
    // Fill in Initialization Code Here.
}};

"""
