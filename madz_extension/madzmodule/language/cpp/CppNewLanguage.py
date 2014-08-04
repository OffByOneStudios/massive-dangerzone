"""madzmodule:module/new/language/cpp/CppNewLanguage.py
@OffbyOne Studios 2014
Class for generating new C++ files.
"""

from madz.bootstrap import *

from madzmodule.language.core import *

@bootstrap_plugin("madzmodule.language.cpp")
class CppNewLanguage(INewLanguage):
    """Class for generating new c++ files"""

    def newlanguage_generate(self, **kwargs):
        """Perform this module operation."""
        return cpp_template.format(**kwargs)

    @classmethod
    def newlanguage_identity(self):
        return "cpp"

    @classmethod
    def newlanguage_extension(self):
        return "cpp"




cpp_template=\
"""/*{namespace}.madz.cpp
* @{author} {date}
* A New Module
*/
#include ".madz/cpp/.wrap-cpp/madz.h"

void MADZOUT::_init(){{
    // Fill in Initialization Code Here.
}};

"""
