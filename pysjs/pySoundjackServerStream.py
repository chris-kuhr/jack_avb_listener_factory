import sys
from random import randint
from scapy.all import *
import time

""" send to multicast group"""
ipdst1 = "192.168.2.16"
ipdst2 = "192.168.188.16"
ipdst3 = "192.168.2.12"
ipdst4 = "192.168.188.19"
sport1 = int (50000)
dport1 = int (50000)
dport_list = [50001]#,50002,50003,50004,50005,50006,50007,50008]

def send8talkers(command="IDLE;"):
    ip = IP ( dst = ipdst4 )
    while True: 
        for port in dport_list:
            dgram = UDP ( sport = port , dport = port )
            ip_packet = ip / dgram / command
            send( ip_packet , iface = "enp0s3")

if __name__ == "__main__":
    # 0xc350 = 50000
    send8talkers("\
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
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;\
")
   
    
    
