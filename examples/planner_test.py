import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))

import madz
import madz.action.planner

madz.action.planner.main()