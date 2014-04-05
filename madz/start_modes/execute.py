import os
import sys
import queue
import threading

import zmq

from ..daemon import client

stdin = sys.stdin.buffer
stdout = sys.stdout.buffer
stderr = sys.stderr.buffer

commqueue = queue.Queue()
stop_event = threading.Event()

# from: http://stackoverflow.com/questions/2554514/asynchronous-subprocess-on-windows
def simple_io_thread(pipe, queue, tag, stop_event):
    """
    Read line-by-line from pipe, writing (tag, line) to the
    queue. Also checks for a stop_event to give up before
    the end of the stream.
    """
    while True:
        line = os.read(pipe.fileno(), 1024)

        while True:
            try:
                # Post to the queue with a large timeout in case the
                # queue is full.
                queue.put((tag, line), block=True, timeout=0.1)
                break
            except Queue.Full:
                if stop_event.isSet():
                    break
                continue
        if stop_event.isSet() or len(line) == 0:
            break

bind_fmt = "tcp://127.0.0.1:{port}"

def start(argv, system, user_config):
    res = client.invoke_minion("execute", (argv[1:], user_config))

    if isinstance(res, str):
        print(res)
        exit(1)

    (in_port, out_port, err_port) = res

    print("Setting up connections: {}, {}, {}".format(in_port, out_port, err_port))

    stdin_thread = threading.Thread(
        target=simple_io_thread,
        args=(stdin, commqueue, "STDIN", stop_event)
    )
    stdin_thread.daemon = True
    stdin_thread.start()

    context = zmq.Context()
    pstdin = context.socket(zmq.PUB)
    pstdout = context.socket(zmq.SUB)
    pstderr = context.socket(zmq.SUB)

    pstdout.setsockopt(zmq.SUBSCRIBE, b'')
    pstderr.setsockopt(zmq.SUBSCRIBE, b'')

    bind_fmt = "tcp://127.0.0.1:{port}"
    pstdin.connect(bind_fmt.format(port=in_port))
    pstdout.connect(bind_fmt.format(port=out_port))
    pstderr.connect(bind_fmt.format(port=err_port))

    joined = False
    finished_out = False
    finished_err = False
    while True:
        try:
            tag, line = commqueue.get(False)
            if tag == "STDIN":
                pstdin.send_pyobj(line)
        except queue.Empty:
            pass

        if not finished_out:
            try:
                out = pstdout.recv_pyobj(zmq.NOBLOCK)
                if len(out) == 0:
                    finished_out = True
                stdout.write(out)
                stdout.flush()
            except zmq.ZMQError:
                pass

        if not finished_err:
            try:
                err = pstderr.recv_pyobj(zmq.NOBLOCK)
                if len(err) == 0:
                    finished_err = True
                stderr.write(err)
                stderr.flush()
            except zmq.ZMQError:
                pass

        if not (finished_out and finished_err):
            continue
        else:
            stop_event.set()
            stdin_thread.join()
            pstdin.close()

            pstdout.close()
            pstderr.close()

            context.term()