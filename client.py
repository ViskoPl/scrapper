# imports

import socket
import sys
import os
from subprocess import call

s = socket.socket()
host = "localhost"
port = 8080


def main():
    s.connect((host, port))
    s.send("Lets begin")


if __name__ == "__main__":
    main()
    s.close()
