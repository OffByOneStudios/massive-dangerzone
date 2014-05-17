import os
import queue
import threading

import zmq

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
        if stop_event.isSet():
            queue.put((tag, ""), block=True)
            break
        
        if len(line) == 0:
            break

class ExecuteStreamSpitterThread(threading.Thread):
    def __init__(self, subproc_control):
        super().__init__()
        self._control = subproc_control

        # Build networking, should probably be done on thread with an event
        self.context = zmq.Context()
        self.stdin = self.context.socket(zmq.SUB)
        self.stdout = self.context.socket(zmq.PUB)
        self.stderr = self.context.socket(zmq.PUB)

        self.stdin.setsockopt(zmq.SUBSCRIBE, b'')

        bind_fmt = "tcp://127.0.0.1:{port}"
        self.stdin.bind(bind_fmt.format(port=self._control.stdin_port))
        self.stdout.bind(bind_fmt.format(port=self._control.stdout_port))
        self.stderr.bind(bind_fmt.format(port=self._control.stderr_port))

    def run(self):
        # Build async subproc communication threads
        commqueue = queue.Queue()
        stop_event = threading.Event()

        procin = self._control.subproc.stdin
        procout = self._control.subproc.stdout
        procerr = self._control.subproc.stderr

        if (procin is None) or (procout is None) or (procerr is None):
            self.stdout.send_pyobj("")
            self.stderr.send_pyobj("")
            self.stdin.close()
            self.stdout.close()
            self.stderr.close()
            return

        stderr_thread = threading.Thread(
            target=simple_io_thread,
            args=(procerr, commqueue, "STDERR", stop_event)
        )
        stdout_thread = threading.Thread(
            target=simple_io_thread,
            args=(procout, commqueue, "STDOUT", stop_event)
        )

        stderr_thread.daemon = True
        stdout_thread.daemon = True

        stderr_thread.start()
        stdout_thread.start()

        # Main loop
        exiting = False
        joined = False
        empty = False
        while True:
            # Forward output
            try:
                tag, line = commqueue.get(False)
                if tag == "STDOUT":
                    self.stdout.send_pyobj(line)
                elif tag == "STDERR":
                    self.stderr.send_pyobj(line)
            except queue.Empty:
                empty = True

            # Forward input
            if not joined:
                try:
                    inp = self.stdin.recv_pyobj(zmq.NOBLOCK)
                    procin.write(inp)
                    procin.flush()
                except zmq.ZMQError:
                    pass
            # Check subproc not finished finished
            if (not (self._control.subproc.returncode is None)) \
                or self._control._minion.banished:
                exiting = True

            # If the subproc is finished we need to join, and then empty the queue
            if exiting:
                if not joined:
                    stop_event.set()
                    self.stdin.close()
                    procin.close()

                    stderr_thread.join()
                    stdout_thread.join()

                    procout.close()
                    procerr.close()

                    joined = True
                    empty = False
                # We have finished, we can exit now:
                elif empty:
                    break;

        self.stdout.close()
        self.stderr.close()
        self.context.term()