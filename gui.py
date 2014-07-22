
import madz

try:
    import zmq
except:
    print("Missing dependency 'ZMQ'")
    exit()
try:
    import PyQt4
    import PyQt4.Qsci
except:
    print("Missing dependency 'PyQt4 (Full Install)'")
    exit()

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__ ), 'examples')))

import tools

start_target = None
if len(sys.argv) > 1:
    start_target = sys.argv[1]

tools.start(start_target)