import sys
from random import randint
from scapy.all import *
import time

# from scapy.contrib.igmpv3 import IGMPv3
# 
# from IGMP_Client import IGMP_Client
# igmpPacket = scapy.contrib.igmp.IGMP()

""" send to multicast group"""
ipdst3 = "192.168.2.12"
ipdst5 = "144.76.81.210"
# ipdst = "239.0.1.1"
sport1 = int (50000) #randint (1024 ,65535)
dport1 = int (50000)

def send8talkers(command="IDLE;"):
    ip = IP ( dst = ipdst5 , ttl=4)
    while True: 
        dgram = UDP ( sport = sport1 , dport = dport1 )
        ip_packet = ip / dgram / command
        send( ip_packet , iface = "enp3s0")
        
        # 1000000÷(256×32) = 122,0703125
        # 1÷122,0703125
        # = 0,0082
        #time.sleep(0.008)

if __name__ == "__main__":
    send8talkers("7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;")

    