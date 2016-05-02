#! /usr/bin/python

import os, sys, time
import vlc, pafy #https://github.com/mps-youtube/pafy
import threading, socket, SocketServer
import json

from urllib import urlencode
from youtube_lib import YouTubePlayer, YouTubeVideo


def search(query):
    import youtube_dl

    search_query = {'search_query': query}
    url = 'https://www.youtube.com/results?' + urlencode(search_query)

    ydl_opts = {'quiet':True, 'max_downloads':10}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url,download=False,process=False)

    names = []
    ids = []

    if 'entries' in result:
        for vid in result['entries']:
            if "/watch?v=" in vid['url']:
                names.append(vid['title'])
                ids.append(vid['url'])
    else:
        names.append(result['title'])
        ids.append(result['url'])

    return {'names':names, 'ids':ids}


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):

        data = self.request.recv(1024).strip()
        if " " not in data:
            data += " "
        print ">> {}".format(data)

        response_data = ""
        response_code = 200

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
                yt_vid = YouTubeVideo.get_instance(args)
                self.server.playlist.append(yt_vid)
                self.server.player.enqueue(yt_vid)
        elif command == "/vol":
            if args:
                self.server.player.set_volume(int(args))
        elif command == "/search":
            if args:
                # print args
                response_code = 300
                response_data = json.dumps(search(args))
        elif command == "/nowplaying":
            response_code = 200
            response_data = self.server.player.get_nowplaying()
            # print response_data
        elif command == "/playlist":
            response_code = 100
            response_data = self.server.player.get_playlist()
        elif command == "/queue":
            response_code = 101
            response_data = self.server.player.get_queue()
        elif command == "/isplaying":
            response_code = 102
            response_data = self.server.player.isPlaying()

        response = "{} {}".format(response_code, response_data)
        self.request.sendall(response)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self, server_address, player, playlist, handler_class=ThreadedTCPRequestHandler):
        self.player = player
        self.playlist = playlist
        if len(self.playlist) > 0:
            for v in playlist:
                self.player.enqueue(v.stream_url)

        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return

if __name__ == "__main__":
    sav_file = 'playlist.sav'

    player = YouTubePlayer()
    playlist = []

    # if os.path.isfile(sav_file):
    #     try:
    #         with open(sav_file) as file:
    #             # pass
    #             # print file.readline()
    #             for line in file:
    #                 # print line
    #                 yt_vid = YouTubeVideo.from_JSON(line)
    #                 print yt_vid.name
    #                 playlist.append(yt_vid)
    #     except IOError as e:
    #         playlist = []

    HOST = ''#sys.argv[1]
    PORT = int(sys.argv[2])
    server = ThreadedTCPServer((HOST, PORT), player, playlist)
    ip, port = server.server_address
    print "Server running at:", ip, port
    server_thread = threading.Thread(name="thr_server", target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name

    try:
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

    # f = open(sav_file, 'w')
    # for video in playlist:
    #     f.write(video.to_JSON())
    #     f.write("\n")
    # f.close()

    print "Bye"
