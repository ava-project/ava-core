#!/usr/bin/python2.7

import socket

socket_addr = "/tmp/ava_socket"

"""
Little client to simulate an interface (write exit to quit the client)
"""
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect(socket_addr)

while True:
    input = raw_input("$> ")
    sock.send(input)
    if input == "exit":
        break

sock.close()
