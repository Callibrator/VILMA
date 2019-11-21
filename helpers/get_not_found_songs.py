#This function will return a list with the songs that were not found! If the sizes of the list do not match, it will return none!

def get_not_found_songs(song_names,songs_f_list):
    if len(song_names) != len(songs_f_list):
        return None

    songs_not_found = []
    for i in range(len(song_names)):
        if songs_f_list[i] == -1:
            songs_not_found.append(song_names[i])


    return songs_not_found
