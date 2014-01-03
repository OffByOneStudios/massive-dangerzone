import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))

import madz
import madz.MDL.parser_impl

madz.MDL.parser_impl.main()