import sys
sys.path.append('C:\\Users\\jibb\\Documents\\AVA\\ava-core')
from demo.Daemon import Daemon
from demo.Event import Event


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

