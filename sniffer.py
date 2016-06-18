#!/usr/bin/python2

import socket
import os

host = "119.29.148.163"

if os.name = "nt":
    socketProtocol = socket.IPPROTO_IP
else:
    socketProtocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socketProtocol)

sniffer.bind((host, 0))

sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

print sniffer.recvfrom(65565)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

def test:
    pass
