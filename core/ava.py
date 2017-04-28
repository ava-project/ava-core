from Daemon import Daemon
from Event import Event

def main():
    print('Launching AVA...')
    daemon = Daemon()
    daemon.run()
    print('AVA is now running, type exit to quit the process or try to execute any command')
    while True:
        try:
            inp = input("$> ")
            if "exit" in inp:
                daemon.stop()
                break
            daemon.add_event(Event(inp, False, 0))
        except KeyboardInterrupt:
            daemon.stop()
        except EOFError:
            daemon.stop()

if __name__ == "__main__":
    main()

