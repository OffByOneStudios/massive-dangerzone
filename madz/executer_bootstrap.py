#!/usr/bin/env python3

## Set up environment:
import sys
import os
import traceback

sys.path.append(os.path.abspath(".."))
bind = sys.argv[1]

## Get libs and objects:

# Operating system loader
import madz.operating_system
mos = madz.operating_system.get_system()

# ZMQ setup:
import zmq
context = zmq.Context()

## Set up listener:

socket = context.socket(zmq.PAIR)
socket.connect(bind)

# The goal of this is to setup an environment where we can call to_execute
to_execute = None
while to_execute is None:
    request = socket.recv_pyobj()

    command = request[0]

    try:
        # Setup execute:
        if command == "execute":
            artifact, index = request[1:3]
            to_execute = mos.get_function(artifact, index)
            socket.send_pyobj(True)

        # Load artifact
        elif command == "load-artifact":
            artifact, state, requires = request[1:4]
            if state == "in-mem":
                mos.load_memory(artifact)
            elif state == "inited":
                mos.load_init(artifact, requires)
            elif state == "final":
                mos.load_final(artifact, requires)
            socket.send_pyobj(True)
        else:
            raise Exception("Unknown command: '{}'!".format(command))
    except:
        tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
        socket.send_pyobj(tb_string)

socket.close()
context.term()

# End of script, bootstrap done!
to_execute()