#!/usr/bin/python3
import os, sys, imp

# Configuration info.
madz_config = {
    "user_config_file": "user_config.py",
    "log_to_stdout": True,
    "logging_file": "./example.log",
    "plugin_directories" : ["./modules/", "./executables/"],
    "plugin_configs" : ["system_config.py"],
}

attached = False
def attach_madz():
    """Add Madz to your system path"""
    global attached
    if not attached:
        os.chdir(os.path.split(os.path.realpath(__file__))[0])
        sys.path.append(os.path.abspath("../../"))
    attached = True

def start_daemon():
    """Start a Madz Server"""
    attach_madz()

    import madz.live_script as madz

    daemon = madz.Daemon(**madz_config)
    print("Configuring Server...")
    daemon.configure()
    print("Starting Server")
    daemon.start()

def create_client():
    attach_madz()
    import madz.live_script as madz
    return madz.Client(madz_config)

def send_kill():
    import madz.live_script as madz
    madz.kill()

def _usage():
    print("Usage: main.py {daemon} | command {command_name} [-p {plugin_namespace}] [-l{log_level}]}")
    exit(1)
        
if __name__ == '__main__':
    if len(sys.argv) == 1:
        _usage()

    attach_madz()

    if sys.argv[1] == "daemon":
        start_daemon()
    
    elif sys.argv[1] == "kill":
        client = create_client()
        client.kill()
    else:
        client = create_client()
        client.run_raw(sys.argv)