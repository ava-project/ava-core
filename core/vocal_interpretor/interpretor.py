import threading
from core.daemon.Event import Event

class Interpretor(object):
    """
    Vocal interpretor encapsulation
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
        self._should_stop = False
        print("### Interpretor running ###")

        while not self._should_stop:
            try:
                inp = input("$> ")
                if "exit" in inp:
                    Interpretor._daemon.stop()
                    break

                Interpretor._daemon.add_event(Event(inp, False, 0))

            except KeyboardInterrupt:
                Interpretor._daemon.stop()
                break

            except EOFError:
                Interpretor._daemon.stop()
                break

        self._should_stop = True
        return

    def run(self):
        """
        """
        self._thread.start()

    def stop(self):
        """
        """
        self._should_stop = True
