#This is an API that controls VLC media player and plays music

import os
import sys
import socket

sys.path.append("./config")
sys.path.append("./helpers")
sys.path.append("./objects")

#Importing My Modules
from Server import Server


server = Server()
server.auto_run()

