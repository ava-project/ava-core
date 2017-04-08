from threading import Thread, Condition
from collections import deque
from subprocess import Popen, PIPE, STDOUT
from Event import Event
import sys

class Daemon:
    def __init__(self):
        self._event_queue = deque([])
        self._th = Thread(None, self.__run)
        self._cv = Condition()
        self._is_running = False

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

    def stop(self):
        self._is_running = False
        self._cv.acquire()
        self._cv.notify()
        self._cv.release()

    def add_event(self, event):
        self._cv.acquire()
        self._event_queue.append(event)
        self._cv.notify()
        self._cv.release()

def main():
    daemon = Daemon()
    daemon.run()
    while True:
        inp = input("$> ")
        if "exit" in inp:
            daemon.stop()
            break
        daemon.add_event(Event(inp, False, 0))

if __name__ == "__main__":
    main()
