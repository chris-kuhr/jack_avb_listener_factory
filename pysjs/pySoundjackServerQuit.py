import sys
from random import randint
from scapy.all import *
import time

""" send to multicast group"""
ipdst1 = "192.168.2.16"
ipdst2 = "192.168.188.16"
ipdst_mc = "224.0.0.22"
sport1 = int (50000)
dport1 = int (50000)
dport_list = [50001]#,50002,50003,50004,50005,50006,50007,50008]

def sendUPDDgram(command="IDLE;"):
    ip = IP ( src = ipdst1, dst = ipdst_mc )
    dgram = UDP ( sport = sport1 , dport = dport1 )
    ip_packet = ip / dgram / command
    send( ip_packet , iface = "enp0s3")
    
if __name__ == "__main__":
    # 0xc350 = 50000
    for port in dport_list:
        sendUPDDgram("QUIT;")
        sendUPDDgram("QUIT;T;%d;"%port)
        sendUPDDgram("QUIT;L;%d;%s;"%(port,ipdst2 ) )
