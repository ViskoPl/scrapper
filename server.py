# imports

import socket
import sys
import os
from subprocess import call

#global values
HOST = "localhost"
PORT = 8080


def bind_socket():
    # trying to bind the socket
    s = bind_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    try:
        s.bind((HOST, PORT))
    except:
    print "Fuck"
    sys.exit()
    return s


def handle_file(conn):
    f = open('test.sdp",'wb')
    call("ffmpeg -i video.mp4 -c:v libvpx -an -f rtp rtp://192.168.1.5:1234 -i video.mp4 -c:a libopus -vn -f rtp rtp://192.168.1.5:1237")
    call("ffmpeg -i video.mp4 -c:v libx264 -an -f rtp rtp://192.168.1.5:1234 -i video.mp4 -c:a aac -vn -f rtp rtp://192.168.1.5:1237")
    call(
        'ffmpeg -f dshow -framerate 30 -i video="HP HD Webcam [Fixed]" -c:v libvpx -an -f rtp rtp://192.168.1.5:1234 -f dshow -i audio="Microphone (2- High Definition Audio Device)" -c:a libopus -vn -f rtp rtp://192.168.1.5:1237')
    call(
        'ffmpeg -f dshow -framerate 30 -i video="HP HD Webcam [Fixed]" -c:v libx264 -an -f rtp rtp://192.168.1.5:1234 -f dshow -i audio="Microphone (2- High Definition Audio Device)" -c:a aac -vn -f rtp rtp://192.168.1.5:1237')


def main():
    # socket
    s = bind_socket()

    s.listen(10)  # 10 connections, as many as you likje

    while(True):
        conn, addr = s.accept()
        print 'Hello', addr
        print "Preparing..."

        os.spawnl(os.P_DETACH, handle_file(conn))


if __name__ == "__main__":
    main()
    s.close()
