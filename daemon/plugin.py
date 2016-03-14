#!/usr/bin/python2.7

import socket
import time
from threading import Thread, RLock
from os import unlink
from subprocess import Popen, PIPE
import os.path

"""
This class allow you to manage your plugins. You just have to create the class with the name
of all you're plugins you want to manage. Then call the methode isActive with the name of
your plugin you want to know if the interface select it.
For an example check below the class declaration
"""
class Plugin():

    def __init__(self, plugins):
        self.socket_addr = "/tmp/ava_socket"
        self.plugins = dict()
        self.mutex = RLock()
        with self.mutex:
            for name in plugins:
                self.plugins[name] = False

    def __enter__(self):
        self.th = Thread(None, self.__run)
        self.th.setDaemon(True)
        self.th.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if os.path.exists(self.socket_addr):
            unlink(self.socket_addr)
        return self

    def __setPlugin(self, pluginName, value):
        with self.mutex:
            if self.plugins.get(pluginName) != None:
                self.plugins[pluginName] = (value == "True" or value == "true")

    def __run(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(self.socket_addr)
        sock.listen(1)
        connection, client_address = sock.accept()

        # print "Connection accepted from %s" % client_address

        while True:
            data = connection.recv(50)
            if data == "dump":
                plugins.dump()
                continue
            if data == "exit":
                break
            cmd = data.split(':')
            if len(cmd) == 2:
                plugins.__setPlugin(cmd[0], cmd[1])

        connection.close()
        sock.close()
        if os.path.exists(self.socket_addr):
            unlink(self.socket_addr)

    def isActive(self, pluginName):
        with self.mutex:
            if self.plugins.get(pluginName) != None:
                return self.plugins[pluginName] == True
            else:
                return False

    def dump(self):
        print self.plugins

"""
====    EXAMPLE    ====
"""

"""
Use the keywork 'with' to ensure object destruction properly
"""

with Plugin(["Atom", "Firefow", "Google-Chrome", "Application Launcher", "Sublime Text"]) as plugins:
    while True:
        inp = raw_input('Tell me something to do: ')
        ws = inp.split(' ')
        if "exit" in ws:
            break
        if "google-chrome" in ws and plugins.isActive("Google-Chrome"):
            process = Popen("google-chrome-stable", shell=True, stdout=PIPE)
            process.wait()
        else:
            print "Unknown instruction"
