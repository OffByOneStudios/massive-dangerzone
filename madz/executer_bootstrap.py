#!/usr/bin/env python3 -u
import sys
import os
import traceback

## Set up environment:
def main(argv):

    print("Starting Bootstrap")
    sys.stdout.flush()

    cwd = argv[1]
    sys.path.append(os.path.join(cwd, ".."))
    bind = argv[2]

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
    command_count = 0
    to_execute = None
    print("Bootstrap accepting commands")
    sys.stdout.flush()
    error_artifacts = []
    while to_execute is None:
        request = socket.recv_pyobj()

        command_count += 1
        if (command_count % 100 == 0):
            sys.stderr.write("Bootstrapped {} commands...\n".format(command_count))
            sys.stderr.flush()

        command = request[0]
        artifact = None
        try:
            # Setup execute:
            if command == "execute":
                artifact, index = request[1:3]
                to_execute = mos.get_function(artifact, index)
            # Load artifact
            elif command == "load-artifact":
                state, artifact, requires = request[1:4]
                if state == "in-mem":
                    mos.load_memory(artifact)
                elif state == "inited":
                    mos.load_init(artifact, requires)
                elif state == "final":
                    mos.load_final(artifact, requires)
                else:
                    raise Exception("Unknown state: '{}'!".format(state))
                socket.send_pyobj(True)
            else:
                raise Exception("Unknown command: '{}'!".format(command))
        except:
            tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
            print(tb_string)
            sys.stdout.flush()
            error_artifacts.append(artifact)
            if (command != "execute"):
                socket.send_pyobj(True) #TODO make false/exception string
            #exit()

    socket.close()
    context.term()

    if len(error_artifacts) != 0:
        print("The following artifacts had errors during bootstraping, exiting:")
        for art in set(error_artifacts):
            print("* {}".format(art))

    print("Starting function {} on artifact {}.".format(index, artifact))
    sys.stdout.flush()
    # End of script, bootstrap done!
    to_execute()

if __name__ == "__main__":
    main(sys.argv)
