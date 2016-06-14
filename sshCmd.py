#!/usr/bin/python2

import threading
import paramiko
import subprocess

def sshCommand(ip, user, passwd, command):
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
        sshSession.exec_command(command)
        print sshSession.recv(1024)
    
    return 

sshCommand("119.29.148.163", "ubuntu", "lanxia2372615", "id")
