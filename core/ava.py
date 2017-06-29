from .daemon.Daemon import Daemon


def main():
    print('Launching AVA...')
    daemon = Daemon()
    daemon.run()
    print('AVA is now running, type exit to quit the process or try to execute any command')


if __name__ == "__main__":
    main()
