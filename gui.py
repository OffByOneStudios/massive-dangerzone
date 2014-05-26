
import madz

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__ ), 'examples')))

import tools

start_target = None
if len(sys.argv) > 1:
    start_target = sys.argv[1]

tools.start(start_target)