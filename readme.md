# VILMA
It is a small server that uses tcp/ip protocol to receive requests from varius devices & clients. It controls vlc player to play music. It may be useful for smart homes or similar cases where you need to control a music station from your smartphone or siri,alex etc... No, I have not developed any alexa skills,mobile apps or anything else yet for controlling the server, I believe that this will be my next step in the future when I find some time!!!

## Installation
### For both linux & windows systems!
first download & install python 3.6
Second, use pip to install all the requirments existing in the requirments.txt file. Command:
```
pip install -r requirments.txt
```

### For Linux:
you will have to download vlc player now. in case you are running ubuntu you can do it by the following command:
```
sudo apt install vlc
```

### For Windows
Download vlc player from its official site. Can be found [here](https://www.videolan.org/vlc/index.html)


## How to run
Execute api.py file

## Configuration Parameters

| Variable | Purpose |
| --- | --- |
| music_folder | The folder where the api will search for music songs! Keep in mind that this folder is only used if you only send the song's name, if you send a full location (song_location parameter) it will search in that exact destination even if it is outside of that specific folder |
| host | the host ip of the server |
| port | the port your server |



## Request example of json object that needs to be send as a string:

```
{
    "command": "play",
    "song_name": "for damaged coda"

}
```


### Possible values for command:
- play: just starts playing music it will play all your songs randomly
- play_song: plays the song described in song_name, if song_location is provided it will not search for the song, it will just try to play the file that is located in the location field
- stop: stops the player
- pause: pauses the player
- resume: resumes the player
- toggle: toggles the player between pause and resume
- next: play next song in the list
- previous: play previous song in the list
- volume: sets volume
- add: adds song the the end of the playlist
- play_next: adds song to next to the song that it is currently playing
- get_songs: returns a list with all songs

## Response Example. It is a json object that will be send to the device/client as string

```
{
    "code":1
    "message": "ok"
    "data": "some data can be here"
}
```

### Return Codes:
- 1 - Everything is fine
- 2 - Can not find the song by either name or location
- 3 - Unknown Error?
- 4 - Basic Parameter(s) Missing
- 5 - Invalid Value for parameter
