#!/usr/bin/python2

import zmq 
import os
import sys

def get_file(path):
    # Set up the zeromq context and socket
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:4545')
    # send the desired file to the server
    socket.send_string(path)

    while True:
        # Start grabing data
        data = socket.recv().decode("utf-8")
        if(data!="fin"):
            print("url: " + data)
        if not socket.getsockopt(zmq.RCVMORE):
            # If there is not more data to send, then break
            break

if __name__ == '__main__':
    get_file(sys.argv[1])
