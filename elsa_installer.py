
import config
import socket
import json

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((config.host,config.port))


example = {
    "action": "add",
    "service_name": "vilma",
    "name": "VILMA",
    "description":"A remote controlled music player",
    "github_rep": "https://github.com/Callibrator/VILMA.git",
    "github_username": "", # Not Email!!!! Just username
    "github_password": "",
    "install_file": "install.bat",
    "execute_file": "execute.bat",
    "startup":"true"

}

exampleStr = json.dumps(example)
exampleLen = len(exampleStr)

s.send(str(exampleLen).encode())

ret = s.recv(2048).decode()
print(ret)
s.send(exampleStr.encode())
retLen = int(s.recv(2048).decode())
s.send(b"ok")
ret = s.recv(retLen)

print("------------")
print(ret.decode())