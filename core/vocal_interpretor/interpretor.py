import threading
from core.daemon.Event import Event

class Interpretor(object):
    """
    AVA vocal interpretor
    """

    def __init__(self, daemon):
        """
        """
        self._should_stop = True
        self._thread = threading.Thread(None, self._run)
        Interpretor._daemon = daemon

    def _run(self):
        """
        """
        while not self._should_stop:
            try:
                inp = input("$> ")
                if "exit" in inp:
                    self._should_stop = True
                    Interpretor._daemon.stop()
                    break
                Interpretor._daemon.add_event(Event(inp, False, 0))
            except KeyboardInterrupt:
                self._should_stop = True
                Interpretor._daemon.stop()
                break
            except EOFError:
                self._should_stop = True
                Interpretor._daemon.stop()
                break

    def run(self):
        """
        """
        self._should_stop = False
        self._thread.start()

    def stop(self):
        """
        """
        self._should_stop = True
