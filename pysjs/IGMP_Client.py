'''
Created on Nov 4, 2016

@author: christoph
'''
import os
import time
import random
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import sendp,srp1,IP,Ether,conf
from scapy.contrib.igmpv3 import IGMPv3

class IGMP_Client:
    def __init__(self,m,g,t,s):
        self.ether = m
        self.group = g
        self.src = s
        self.timeOut = t
        self.join()
    #---------------------------------------------------------------------------------------
        
    def ipToMac(self, addy, mcast=0):
        if(mcast):
            mac = "01:00:5e"
        else:
            mac = "00:00:00"
    
        octets = addy.split(".")
        for x in range(1,4):
            num = str(hex(int(octets[x])))
            num =  num.split("x")[1]
            if len(num) < 2:
                num = "0" + str(num)
            mac += ":" + num
        return mac
    #---------------------------------------------------------------------------------------
  
    def refresh(self,g,t):
        self.leave()
        self.group = g
        self.timeOut = t
        self.join()
    #---------------------------------------------------------------------------------------
        
    def join(self):
        print("Joining " + self.group + " from " + self.src + " t=" + str(self.timeOut))
        
        l2 = Ether(dst=self.ipToMac(self.group,1), src=self.ether, type=0x800)
        l3 = IP(proto=2, ttl=1, src=self.src, dst=self.group)
        l4 = IGMPv3(gaddr=self.group, type=0x11)
        l4.srcaddrs = ['192.168.188.67', '192.168.188.11']
        l4.igmpize(ip=l3, ether=l2)
        sendp(l2/l3/l4)
    #---------------------------------------------------------------------------------------
    
    def leave(self):
        print("Leaving " + self.group + " from " + self.src)
        l2 = Ether(dst="01:00:5e:00:00:02", src=self.ether, type=0x800)
        l3 = IP(proto=2, ttl=1, src=self.src, dst="224.0.0.2")
        l4 = IGMPv3(gaddr=self.group, type=0x17)
        sendp(l2/l3/l4)
    #---------------------------------------------------------------------------------------
#=========================================================================================================


    
    
    