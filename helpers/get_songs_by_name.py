#This function will return a list of songs filepaths that match a name or an empty list if it does not find any songs. It accepts regular Expresions as names of songs!
#Arguments:
# 1 - name: name of the song
# 2 - folder_directory_to_search

import os
import re
def get_songs_by_name(name,folder):

    songs = []
    other_dirs = [os.sep]

    i = 0

    while i < len(other_dirs):
        if i == 0:
            current_dir = folder + other_dirs[i]
        else:
            current_dir =other_dirs[i]

        for fname in os.listdir(current_dir):
            current_path = current_dir

            if current_path[-1] != os.sep:
                current_path += os.sep+fname
            else:
                current_path += fname

            if os.path.isdir(current_path):
                other_dirs.append(current_path)
            elif os.path.isfile(current_path):
                res = re.search(name.lower(),fname.lower())
                if res:
                    songs.append(current_path)




        i += 1

    return songs

if __name__ == "__main__":
    res = get_songs_by_name("r*",r"F:\MyData\Music")
    print(res)

