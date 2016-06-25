#!/usr/bin/python2

import socket
import paramiko
import threading
import sys

hostKey = paramiko.RSAKey(filename = "testRsa.key")

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

        def check_auth_password(self, username, password):
            if (username == "ubuntu") and (password == "lanxia2372615"):
                return paramiko.AUTH_SUCCESSFUL
            
            return paramiko.AUTH_FAILED

server = sys.argv[1]
sshPort = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, sshPort))
    sock.listen(100)

    print "[+] Listening for connection ..."
    client, addr = sock.accept()
except Exception, e:
    print '[-] Listen failed: ' + str(e)
    sys.exit(1)

print '[+] Got a connection!'

try:
    session = paramiko.Transport(client)
    session.add_server_key(hostKey)
    server = Server()
