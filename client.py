#! /usr/bin/python

import socket, sys, json

HOST = ""
PORT = 0

def search(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        if " " not in response:
            response += " "
        status_code, data = response.split(' ', 1)

        if status_code == '300':  # is a search return
            data = json.loads(data)

            times = data['times']
            names = data['names']
            ids = data['ids']

            for i in range(0,len(ids)):
                print "[", i, "] - ", names[i], times[i]

            user_response = len(ids)+1
            while int(user_response) not in range(0,len(ids)):
                user_response = raw_input('Select your choice: ')
            choice = int(user_response)

            text = "Do you wish to add " + names[choice] + " to the playlist? (y/n) "
            user_response2 = raw_input(text)
            if user_response2 == 'y':
                send("/add " + "https://www.youtube.com/watch?v=" + ids[choice])
            else:
                print "Not added"
    finally:
        sock.close()

def send(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
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
def debug():
    send("/add https://www.youtube.com/watch?v=_V7ZKk-NJVA")
    send("/add https://www.youtube.com/watch?v=aqXW57WM9TA")
    send("/play ")
    send("/next ")
    # send(HOST, PORT, "/add https://www.youtube.com/watch?v=niex6_vZcdA")
    # send(HOST, PORT, "/add https://www.youtube.com/watch?v=i_kF4zLNKio")
    # send(HOST, PORT, "/add https://www.youtube.com/watch?v=ntuxR5q-N0M")
    # send(HOST, PORT, "/add https://www.youtube.com/watch?v=1TX5gsKBo88")
    # send(HOST, PORT, "/add https://www.youtube.com/watch?v=8ELbX5CMomE")
    # send(HOST, PORT, "/vol 20")

def main():
    global HOST
    global PORT
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    debug()

    while True:
        msg = raw_input('>> ')
        if msg == "/quit" or msg == "/q":
            break
        elif msg.startswith("/search"):
            search(msg)
        send(msg)
    print 'bye'


if __name__ == '__main__':


    main()
