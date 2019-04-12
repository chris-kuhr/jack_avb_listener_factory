import sys
from random import randint
from scapy.all import *
import time

# from scapy.contrib.igmpv3 import IGMPv3
# 
# from IGMP_Client import IGMP_Client
# igmpPacket = scapy.contrib.igmp.IGMP()
class AVDECC(Packet):
    name = "AVDECCPacket "    
    fields_desc=[ XByteField("cd_subtype",0xfa) ,
                 XByteField("sv_avb_version_msg_type",0x00) ,
                 XByteField("valid_time_data_length_hi",0x00) ,
                 XByteField("data_length_lo",0x00)  ]
    
class ADP(Packet):
    name = "ADPPacket "  
    fields_desc=[ XLongField("entity_guid",0xfedcba9876543210) ,
                 XIntField("vendor_id",0x76543210) ,
                 XIntField("model_id",0x76543210) ,
                 XIntField("entity_capabilities",0x76543210) ,
                 XShortField("talker_stream_sources",0x3210) ,
                 XShortField("talker_capabilities",0x3210) ,
                 XShortField("listener_stream_sinks",0x3210) ,
                 XShortField("listener_capabilites",0x3210) ,
                 XIntField("controller_capabilities",0x76543210) ,
                 XIntField("available_index",0x76543210) ,
                 XLongField("as_grandmaster_id",0xfedcba9876543210) ,
                 XIntField("default_audio_format",0x76543210) ,
                 XIntField("default_video_format",0x76543210) ,
                 XLongField("association_id",0xfedcba9876543210) ,
                 XIntField("entity_type",0x76543210)  ]
    
#     fields_desc=[ ShortField("mickey",5),
#                  XByteField("minnie",3) ,
#                  IntEnumField("donald" , 1 ,
#                       { 1: "happy", 2: "cool" , 3: "angry" } ) ]
    
    
""" send to multicast group"""
ipdst1 = "192.168.13.10"
ipdst2 = "192.168.13.2"
ipdst3 = "192.168.188.19"
ipdst_mc = "224.0.0.22"
# ipdst = "239.0.1.1"
sport1 = int (50000) #randint (1024 ,65535)
dport1 = int (50000)
dport_list = [50001,50002,50003,50004,50005,50006,50007,50008]

def sendUPDDgram(command="IDLE;"):
    ip = IP ( src = "192.168.188.16", dst = ipdst_mc )
    dgram = UDP ( sport = sport1 , dport = dport1 )
    ip_packet = ip / dgram / command
    send( ip_packet , iface = "enp0s3")
    
def sendUPDDgramPeriodically(command="IDLE;"):
    ip = IP ( dst = ipdst3 )
    dgram = UDP ( sport = sport1 , dport = dport1 )
    ip_packet = ip / dgram / command
    send( ip_packet , iface = "enp0s3", inter=0.01, loop=1)


def send8talkers(command="IDLE;"):
    ip = IP ( dst = ipdst3 )
    while True: 
        for port in dport_list:
            dgram = UDP ( sport = port , dport = port )
            ip_packet = ip / dgram / command
            send( ip_packet , iface = "enp0s3")
        time.sleep(0.01)

# def igmpJoin():
#     a = Ether( src = "a0:36:9f:3f:be:a3" )
#     b = IP( src = "192.162.13.2" )
#     c = IGMP( type = 0x12, gaddr = "224.2.3.4" )
#     c.igmpize( b, a )
#     print("Joining IP " + c.gaddr + " MAC " + a.dst )
#     sendp( a/b/c, iface = "eth0" )


if __name__ == "__main__":
#     for port in dport_list:
#         sendUPDDgram("CREATE;T;%d;"%port)
#     send8talkers("7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;7f7f7f7f;")

    eth = Ether( dst = "91:e0:f0:01:00:00", type = 0x22f0)
    avdecc = AVDECC()
    adp = ADP()
    
    discover = eth / avdecc / adp
    sendp( discover  , iface = "enp3s0")
    
    
    
    