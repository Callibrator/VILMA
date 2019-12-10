#This is the server, it will be used as an API!
#The server gets one request and sends one response, then it closes the socket!
#The server waits for a json string request with the following parameters: command, song_name, song_location,value

'''
request example

{
    "command": "play",
    "song_name": "for damaged coda"

}

Possible values for command:
    play: just starts playing music it will play all your songs randomly
    play_song: plays the song described in song_name, if song_location is provided it will not search for the song, it will just try to play the file that is located in the location field
    stop: stops the player
    pause: pauses the player
    resume: resumes the player
    toggle: toggles the player between pause and resume
    next: play next song in the list
    previous: play previous song in the list
    volume: sets volume
    add: adds song the the end of the playlist
    play_next: adds song to next to the song that it is currently playing
    get_songs: returns a list with all songs
    status: returns a json object that describes the current status of the player!


Possible values for song_name:
    all possible strings. This field is used by play,add,play_next. It searches for the song name in the specified folder of your music and its subfolders! This value is treated as a regular expression!

possible values for song_location
    all possible strings. If this field exists the song_name is ignored by play,add,play_next and it uses this as the standard location of the file!

possible values for value:
    all numbers existing in R! It is used by volume command to set the volume of the player!

'''

'''
response example

{
    "code":1
    "message": "ok"
    "data": "some data can be here"
}

Possible Codes
1 - Everything is fine
2 - Can not find the song by either name or location
3 - Unknown Error?
4 - Basic Parameter(s) Missing
5 - Invalid Value for parameter

'''


import socket
import config
from get_songs_by_name import get_songs_by_name
import json
from VlcPlayer import VlcPlayer
import random
from get_not_found_songs import get_not_found_songs

class Server():
    def __init__(self):
        self.host = config.host
        self.port = config.port

    def init_server(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.bind((self.host,self.port))
        self.socket.listen(10)

        self.player = VlcPlayer()


    def active_server(self):

        while True:
            client,addr = self.socket.accept()
            client.settimeout(0.9)

            #Receiving Data
            data = ""

            try:
                temp_data = client.recv(2048).decode()
                client.send(b"ok")
                temp_data = client.recv(int(temp_data))

            except:
                temp_data = ""


            data = temp_data


            try:
                respObject = json.loads(data)
            except:
                respObject = None

            if respObject != None:

                code = self.request_handler(respObject)
            else:
                code = self.generate_response_from_code(4)

            try:
                serialData = json.dumps(code).encode()
                client.sendall(str(len(serialData)).encode())
                res = client.recv(2048).decode()
                if res == "ok":
                    client.sendall(serialData)
                client.close()

            except:
                print("Error Closing Client")
                pass




    def auto_run(self):
        self.init_server()
        self.active_server()

    def request_handler(self,response):

        if not "command" in response:
            return self.generate_response_from_code(4)

        if response["command"].lower() == "play":
            songs = get_songs_by_name(".*",config.music_folder)
            random.shuffle(songs)
            ret = self.player.play_song(songs)
            nf = get_not_found_songs(songs,ret)

            if len(nf) == len(songs):
                return self.generate_response_from_code(2)
        elif response["command"].lower() == "play_song":
            if "song_location" in response:
                ret = self.player.play_song(response["song_location"])
                if ret == -1:
                    return self.generate_response_from_code(2)

            elif "song_name" in response:
                songs = get_songs_by_name(response["song_name"],config.music_folder)
                ret = self.player.play_song(songs)
                nf = get_not_found_songs(songs,ret)
                if len(nf) == len(songs):
                    return self.generate_response_from_code(2)
            else:
                return self.generate_response_from_code(4)


        elif response["command"].lower() == "stop":
            self.player.stop()
        elif response["command"].lower() == "pause":
            self.player.pause()
        elif response["command"].lower() == "resume":
            self.player.resume()

        elif response["command"].lower() == "toggle":
            self.player.toggle()

        elif response["command"].lower() == "next":
            self.player.next()

        elif response["command"].lower() == "previous":
            self.player.previous()
        elif response["command"].lower() == "volume":
            if "value" in response:
                try:
                    value = int(response["value"])
                except:
                    return self.generate_response_from_code(5)

                self.player.set_volume(value)
            else:
                return self.generate_response_from_code(4)

        elif response["command"].lower() == "add":

            if "song_location" in response:
                ret = self.player.add_song_end(response["song_location"])
                self.player.start()
                if ret == -1:
                    return self.generate_response_from_code(2)

            elif "song_name" in response:
                songs = get_songs_by_name(response["song_name"],config.music_folder)
                ret = self.player.add_song_end(songs)
                self.player.start()
                nf = get_not_found_songs(songs,ret)
                if len(nf) == len(songs):
                    return self.generate_response_from_code(2)
            else:
                return self.generate_response_from_code(4)



        elif response["command"].lower() == "play_next":

            if "song_location" in response:
                ret = self.player.add_song(response["song_location"])
                self.player.start()
                if ret == -1:
                    return self.generate_response_from_code(2)

            elif "song_name" in response:
                songs = get_songs_by_name(response["song_name"],config.music_folder)
                ret = self.player.add_song(songs)
                self.player.start()
                nf = get_not_found_songs(songs,ret)
                if len(nf) == len(songs):
                    return self.generate_response_from_code(2)
            else:
                return self.generate_response_from_code(4)
        elif response["command"].lower() == "get_songs":
            songs = get_songs_by_name(".*",config.music_folder)
            ret = self.generate_response_from_code(1)
            ret["data"] = songs
            return ret
        elif response["command"].lower() == "status":
            results = self.player.get_status()
            ret = self.generate_response_from_code(1)
            ret["data"] = results
            return ret

        else:
            return self.generate_response_from_code(4)

        return self.generate_response_from_code(1)

    def generate_response_from_code(self,code):
        data = {}
        data["code"] = code
        if code == 1:
            data["message"] = "Status Ok!"
        elif code == 2:
            data["message"] = "Can not find the song by either name or location"
        elif code == 3:
            data["message"] = "Operation Failed For Unknown Reasons"
        elif code == 4:
            data["message"] = "One or more basic parameters are missing"
        elif code == 5:
            data["message"] = "One or more parameters have an invalid value"
        else:
            data["message"] = "Unknown Code!"

        return data









