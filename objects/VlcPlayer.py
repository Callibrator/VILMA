#This is a vlc Player, it will contain all that I need to control the player


#Functions:
# play_song - a string with the song filepath as argument or a list with multiple song filepaths as arguments. It will immediately start playing that song or those songs
# stop,start,pause functions: they take no arguments and the do what they say exactly
# add_song - takes a string that show the location of the song or a list of string that show location of multiple songs and add them next to the current song
# add_song_end - takes a string that show the location of the song or a list of string that show location of multiple songs and add them next to the last song in the list
# all functions that you need to provide arguments -1 if they do not find the song(s). In case you provide a list songs, it will return an array 0 for songs found and -1 for songs it does not find!

#__get_playing_media Returns the media and its index currently playing or None if not found

import vlc
import time
import os

class VlcPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_list_player_new()
        self.media_list = self.instance.media_list_new()

        self.player.set_media_list(self.media_list)

    def play_song(self,song_path):

        current_song_index = self.get_playing_media()

        if current_song_index != None:
            current_song_index = current_song_index["index"] + 1

        else:
            current_song_index = 0

        ret_value = 0
        if type(song_path) == type([]):
            i = 0
            pos = current_song_index
            ret_value = []
            for song in song_path:
                if os.path.isfile(song):
                    ret_value.append(0)
                else:
                    ret_value.append(-1)
                    continue


                media = self.instance.media_new(song)

                self.media_list.insert_media(media,pos)
                if i == 0:
                    self.player.play_item_at_index(current_song_index)
                i += 1
                pos += 1

        else:
            if not os.path.isfile(song_path):
                    ret_value = -1
            else:
                media = self.instance.media_new(song_path)

                self.media_list.insert_media(media,current_song_index)
                self.player.play_item_at_index(current_song_index)

        self.start()
        return ret_value

    def get_playing_media(self):

        if not self.player.is_playing():
            return None

        for i in range(self.media_list.count()):
            media = self.media_list.item_at_index(i)
            state = media.get_state()
            print(state,i)
            if vlc.State.Playing == state or vlc.State.Opening == state or vlc.State.Stopped == state or vlc.State.Paused == state or vlc.State.Buffering == state:
                return {
                    "media": media,
                    "index": i
                }

            i += 1
        return None

    def add_song(self,song_path):
        current_song_index = self.get_playing_media()
        if current_song_index != None:
            current_song_index = current_song_index["index"] + 1
        else:
            current_song_index = 0
        ret_value = 0
        if type(song_path) == type([]):
            i = 0
            pos = current_song_index
            ret_value = []
            for song in song_path:
                if os.path.isfile(song):
                    ret_value.append(0)
                else:
                    ret_value.append(-1)
                    continue

                media = self.instance.media_new(song)

                self.media_list.insert_media(media,pos)
                i += 1
                pos += 1

        else:
            if not os.path.isfile(song_path):
                    ret_value = -1
            else:
                media = self.instance.media_new(song_path)
                self.media_list.insert_media(media,current_song_index)

        return ret_value

    def add_song_end(self,song_path):

        ret_value = 0
        if type(song_path) == type([]):
            ret_value = []
            for song in song_path:
                if os.path.isfile(song):
                    ret_value.append(0)
                else:
                    ret_value.append(-1)
                    continue

                media = self.instance.media_new(song)

                self.media_list.add_media(media)
        else:
            if not os.path.isfile(song_path):
                    ret_value = -1
            else:
                media = self.instance.media_new(song_path)
                self.media_list.add_media(media)
        return ret_value
    def stop(self):
        self.player.stop()

    def start(self):
        if not self.player.is_playing():
            self.player.play()

    def pause(self):
        self.player.set_pause(1)

    def resume(self):
        self.player.set_pause(0)

    def toggle(self):
        self.player.pause()

    def next(self):
        self.player.next()

    def previous(self):
        self.player.previous()

    def set_volume(self,volume):
        try:
            vol = float(volume)
        except:
            vol = 50

        if vol > 100:
            vol = 100
        if vol < 0:
            vol = 0

        self.player.get_media_player().audio_set_volume(int(vol))


if __name__ == "__main__":
    v = VlcPlayer()
    v.add_song('F:\\MyData\\Music\\America\\America - The Complete Greatest Hits - 01 - A Horse With No Name.mp3')
    v.add_song_end('F:\\MyData\\Music\\America\\America - The Complete Greatest Hits - 02 - Sandman.mp3')
    v.add_song_end(r'F:\MyData\Music\Chaos Chaos - 2014 - Committed to the crime\Chaos Chaos - 01 - Love.flac')
    v.add_song_end(r'F:\MyData\Music\Chaos Chaos - 2014 - Committed to the crime\Chaos Chaos - 02 - Breaker.flac')
    v.add_song_end(r'F:\MyData\Music\Chaos Chaos - 2014 - Committed to the crime\Chaos Chaos - 03 - Do You Feel It-.flac')
    v.add_song_end(r'F:\MyData\Music\Chaos Chaos - 2014 - Committed to the crime\Chaos Chaos - 04 - West Side.flac')
    v.add_song_end(r'F:\MyData\Music\Chaos Chaos - 2014 - Committed to the crime\Chaos Chaos - 05 - Monsters.flac')
    v.start()
    time.sleep(5)

    v.pause()
    v.pause()
    time.sleep(3)
    print("Ressuming")
    v.resume()
    v.resume()


    print(v.get_playing_media())
    time.sleep(600)
    print("Second Song Added")


    v.play_song(r'F:\MyData\Music\blonde redhead\Melody Of Certain Damaged Lemons\11 For The Damaged Coda.mp3')



    while True:
        time.sleep(5)
        print(v.media_list.count())
        print(v.media_list.media())
        print(v.get_playing_media())
