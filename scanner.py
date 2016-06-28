#!/usr/bin/python2

import socket
import os
import struct
import threading

from netaddr import IPNetwork, IPAddress
from ctypes import *

host = "119.29.148.163"

subnet = "192.168.0.0/24"

magicMsg = "PythonRules"

def udpSender(subnet, magicMsg):
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    for ip in IPNetwork(subnet):
        try:
            sender.sendto(magicMsg, ("%s" % ip, 65212))
        except:
            pass

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

t = threading.Thread(target = udpSender, args = (subnet, magicMsg))
t.start()

try:
    while True:
        
        rawBuffer = sniffer.recvfrom(65565)[0]
        ipHeader = IP(rawBuffer[0:20])

        if ipHeader.protocol == "ICMP":
            offset = ipHeader.ihl * 4
            buf = rawBuffer[offset:offset + sizeof(ICMP)]

            icmpHeader = ICMP(buf)

            if icmpHeader.code == 3 and icmpHeader.type == 3:
                if IPAddress(ipHeader.src_address) in IPNetwork(subnet):
                    if rawBuffer[len(rawBuffer) - len(magicMsg):] == magicMsg:
                        print "Host Up: %s" % ipHeader.src_address

except KeyboardInterrupt:
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

