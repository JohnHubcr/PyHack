#!/usr/bin/python2

import socket
import os
import struct
from ctypes import *

host = "119.29.148.163"

class IP(Structure):
    
    _fields_ = [
        ("ihl", c_ubyte, 4),
        ("version", c_ubyte, 4),
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_num", c_ubyte),
        ("sum", c_ushort),
        ("src", c_ulong),
        ("dst", c_ulong)
    ]

    def __new__(self, socketBuffer = None):
        return self.from_buffer_copy(socketBuffer)

    def __init__(self, socketBuffer = None):
        
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}

        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))
        
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

if os.name == "nt":
    socketProtocol = socket.IPPROTO_IP
else:
    socketProtocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socketProtocol)

sniffer.bind((host, 0))

sniffer.setsockopt(socket.IPPROTO_I, socket.IP_HDRINCL, 1)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

try:
    while True:
        rawBuffer = sniffer.recvfrom(65565)[0]
        
        ipHeader = IP(rawBuffer[0:20])
        
        print "Protocol: %s %s -> %s" % (ipHeader.protocol, ipHeader.src_address, ipHeader.dst_address)

except KeyboardInterrupt:
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
