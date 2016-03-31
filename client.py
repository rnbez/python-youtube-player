#! /usr/bin/python

import socket, sys

def send(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        if " " not in response:
            response += " "
        status_code, data = response.split(' ', 1)
        return status_code
        # print "Received: {}".format(response)
    finally:
        sock.close()


def main():
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    while True:
        msg = raw_input('>> ')
        send(HOST, PORT, msg)
        if msg == "/quit" or msg == "/q":
            break
    print 'bye'


if __name__ == '__main__':
    # HOST = sys.argv[1]
    # PORT = int(sys.argv[2])
    # send(HOST, PORT, "/add https://www.youtube.com/watch?v=1TX5gsKBo88")
    # send(HOST, PORT, "/play ")
    # send(HOST, PORT, "/add https://www.youtube.com/watch?v=niex6_vZcdA")
    # send(HOST, PORT, "/add https://www.youtube.com/watch?v=aqXW57WM9TA")
    # send(HOST, PORT, "/add https://www.youtube.com/watch?v=i_kF4zLNKio")
    # send(HOST, PORT, "/add https://www.youtube.com/watch?v=ntuxR5q-N0M")
    # send(HOST, PORT, "/add https://www.youtube.com/watch?v=_V7ZKk-NJVA")
    # send(HOST, PORT, "/add https://www.youtube.com/watch?v=8ELbX5CMomE")
    main()
