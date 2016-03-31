import sys, vlc, pafy #https://github.com/mps-youtube/pafy
from Queue import Queue

class YouTubeVideo:
    def __init__(self):
        self.name = ""
        self.url = ""
        self.stream_url = ""
        self.duration = 0

class YouTubePlayer:
    def __init__(self):
        self.queue = Queue()
        self.is_stopped = False
        self.is_media_set = False
        self.instance = vlc.Instance('--no-fullscreen --autoscale --quiet')
        self.playlist = self.instance.media_list_new()
        self.player = self.instance.media_list_player_new()
        self.player.set_media_list(self.playlist)
        self.event_manager = self.player.event_manager()
        # self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.end_callback)
        # self.event_manager.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.pos_callback)

        # self.playlist.lock()
        # self.playlist.add_media(self.instance.media_new("vid_work.mp4"))
        # self.playlist.add_media(self.instance.media_new("vid_dirt_off_your_shoulder.mp4"))
        # self.playlist.add_media(self.instance.media_new("vid_sorry.mp4"))
        # print "playlist size is now", self.playlist.count()
        # self.playlist.unlock()

    def play(self):
        if not self.player.is_playing():
            # if not self.is_media_set:
            #     url = str(self.queue.get())
            #     video = pafy.new(url)
            #     url = video.getbest().url
            #     # self.playlist.add_media(self.instance.media_new(url))
            #     # self.player.set_media(self.instance.media_new(url))
            #     self.queue.task_done()
            #     self.is_media_set = True
            self.player.play()
        return
    def pause(self):
        # if self.is_playing:
        self.player.pause()
        return
    def stop(self):
        self.player.stop()
        self.is_stopped = True
        return
    def next(self):
        self.player.next()
        # print "next video"
        # if self.is_stopped:
        #     self.stop()
        # if not self.queue.empty():
        #     url = str(self.queue.get(False))
        #     self.queue.task_done()
        #     print "next url is", url
        #     video = pafy.new(url)
        #     print "fetching url"
        #     url = video.getbest().url
        #     print "setting new media"
        #     # self.playlist.add_media(self.instance.media_new(url))
        #     # self.player.set_media(self.instance.media_new(url))
        #     self.is_media_set = True
        #     print "strating new video"
        #     self.player.play()
        # return
    def enqueue(self, url):
        self.queue.put(url)

        video = pafy.new(url)
        url = video.getbest().url

        self.playlist.lock()
        self.playlist.add_media(self.instance.media_new(url))
        print "playlist size is now", self.playlist.count()
        self.playlist.unlock()

        arr = [url for url in self.queue.queue]
        print "QUEUE:"
        index = 1
        for url in arr:
            print "  ", index, ": ", url
            index += 1
        return

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
    pass
if __name__ == '__main__':
    main()
