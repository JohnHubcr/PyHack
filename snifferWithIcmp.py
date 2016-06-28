#!/usr/bin/python2

import socket
import os
import struct
import threading

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

class ICMP(Structure):
    
    _fields_ = [
        ("types", c_ubyte),
        ("code", c_ubyte),
        ("checksum", c_ushort),
        ("unused", c_ushort),
        ("next_hop_mtu", c_ushort)
    ]

    def __new__(self, socketBuffer):
        return self.from_buffer_copy(socketBuffer)

    def __init__(self, socketBuffer):
        pass


if os.name == "nt":
    socketProtocol = socket.IPPROTO_IP
else:
    socketProtocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))

sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

try:
    while True:
        
        rawBuffer = sniffer.recvfrom(65565)[0]
        
        ipHeader = IP(rawBuffer)
        
        print "Protocol: %s %s -> %s" % (ipHeader.protocol, ipHeader.src_address, ipHeader.dst_address)

        if ipHeader.protocol == "ICMP":
            
            offset = ipHE.ihl * 4
            buf = rawBuffer[offset:offset + sizeof(ICMP)]
            
            icmpHeader = ICMP(buf)

            print "ICMP -> Type: %d Code: %d" % (icmpHeader.type,icmpHeader.code)

except KeyboardInterrupt:
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
