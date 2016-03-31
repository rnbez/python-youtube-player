#! /usr/bin/python

import sys, time
import vlc, pafy #https://github.com/mps-youtube/pafy
import threading, socket, SocketServer

from Queue import Queue
from youtube_lib import YouTubePlayer, YouTubeVideo

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):

        data = self.request.recv(1024).strip()
        if " " not in data:
            data += " "
        print ">> {}".format(data)

        command, args = data.split(' ', 1)
        if command == "/play":
            # if args:
            #     video = pafy.new(args)
            #     url = video.getbest().url
            #     self.server.player.set_media(instance.media_new(url))
            self.server.player.play()
        elif command == "/pause":
            self.server.player.pause()
        elif command == "/next":
            self.server.player.next()
        elif command == "/add":
            if args:
                self.server.player.enqueue(args)
        data = ""
        response = "{} {}".format(200, data)
        self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self, server_address, player, handler_class=ThreadedTCPRequestHandler):
        self.player = player
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return

if __name__ == "__main__":
    # instance = vlc.Instance('--no-fullscreen')
    # url = "https://www.youtube.com/watch?v=OPf0YbXqDm0"
    # video = pafy.new(url)
    # movie = video.getbest().url
    # player = instance.media_player_new()
    player = YouTubePlayer()

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    # HOST, PORT = "localhost", 9995
    server = ThreadedTCPServer((HOST, PORT), player)
    ip, port = server.server_address
    print "Server running at:", ip, port
    server_thread = threading.Thread(name="thr_server", target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name

    try:
        # player.set_media(instance.media_new(movie))
        # player.play()
        # player.pause()
        while True:
            pass
    except KeyboardInterrupt:
        print "\nServer Interrupted"

    print "stopping player"
    player.stop()
    print "shutting down"
    server.shutdown()
    print "closing server"
    server.server_close()
    print "Bye"
