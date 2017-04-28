from threading import Thread, Condition
from collections import deque
from subprocess import Popen, PIPE
import sys
from DaemonServer import DaemonServer

class Daemon:
    def __init__(self):
        self._event_queue = deque([])
        self._th = Thread(None, self.__run)
        self._cv = Condition()
        self._is_running = False
        self._ds = DaemonServer("http://163.5.84.224:80")

    def __run(self):
        while self._is_running:
            while len(self._event_queue) != 0:
                self.__exec()
            else:
                self._cv.acquire()
                self._cv.wait()

    def __exec(self):
        event = self._event_queue.popleft()
        process = Popen(event.get_cmd(), shell=True, stdout=PIPE)
        process.wait()
        out, err = process.communicate()
        if err is not None:
            print(err.decode(sys.stdout.encoding))
        print(out.decode(sys.stdout.encoding))

    def run(self):
        self._is_running = True
        self._th.start()
        self._ds.run()

    def stop(self):
        self._is_running = False
        self._cv.acquire()
        self._cv.notify()
        self._cv.release()
        self._ds.stop()

    def add_event(self, event):
        self._cv.acquire()
        self._event_queue.append(event)
        self._cv.notify()
        self._cv.release()
