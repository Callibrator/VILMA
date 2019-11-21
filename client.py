from socket import *
import sys
import json

sys.path.append("./config")

import config

s = socket(AF_INET,SOCK_STREAM)

s.connect((config.host,config.port))

t1 = {
    "command": "pause",
    "song_name": "Linkin Park - What I've Done",
    "value": 100
}

str_data = json.dumps(t1)

s.sendall(str_data.encode())


ret = s.recv(2048)

print(ret.decode())
print("Done!")


