import sys, vlc, pafy #https://github.com/mps-youtube/pafy
import json

class YouTubeVideo():
    def __init__(self, name = '', url = '', stream_url = '', duration = '', owner = 'anonymous'):
        self.name = name
        self.url = url
        self.stream_url = stream_url
        self.duration = duration
        self.owner = owner

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)#, indent=2)

    @staticmethod
    def from_JSON(data):
        data = json.loads(data)
        titl = data["name"]
        url = data["url"]
        str_u = data["stream_url"]
        dur = data["duration"]
        ownr = data["owner"]

        return YouTubeVideo(titl, url, str_u, dur, ownr)

    @staticmethod
    def get_instance(url):
        video = pafy.new(url)
        titl = video.title
        url = url
        str_u = video.getbest().url
        dur = video.duration

        return YouTubeVideo(titl, url, str_u, dur)


class YouTubePlayer:
    def __init__(self):
        self.instance = vlc.Instance('--no-fullscreen', '--autoscale', '--quiet')
        self.playlist = self.instance.media_list_new()
        self.player = self.instance.media_list_player_new()
        self.player.set_media_list(self.playlist)
        self.event_manager = self.player.event_manager()

    def play(self):
        self.player.play()
        return
    def pause(self):
        self.player.pause()
        return
    def stop(self):
        self.player.stop()
        return
    def next(self):
        self.player.next()
    def enqueue(self, url):
        # video = pafy.new(url)
        # url = video.getbest().url
        self.playlist.lock()
        self.playlist.add_media(self.instance.media_new(url))
        # print "playlist size is now", self.playlist.count()
        self.playlist.unlock()

        # arr = [url for url in self.queue.queue]
        # print "QUEUE:"
        # index = 1
        # for url in arr:
        #     print "  ", index, ": ", url
        #     index += 1
        # return

    @vlc.callbackmethod
    def end_callback(self, event):
        self.next()

    @vlc.callbackmethod
    def pos_callback(self, event):
        # if echo_position:
        # sys.stdout.write('\r%s to %.2f%% (%.2f%%)' % (event.type,
        #                                               event.u.new_position * 100,
        #                                               player.get_position() * 100))
        # sys.stdout.flush()
        pass




def main():
    # pass
    video = YouTubeVideo.get_instance("https://www.youtube.com/watch?v=bpOSxM0rNPM")
    print video.to_JSON()
    # video = YouTubeVideo.from_JSON(video.to_JSON())
    # print video.name

if __name__ == '__main__':
    main()
