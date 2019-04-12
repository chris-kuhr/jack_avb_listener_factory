from scapy.all import *


from AVDECC_Packet import * #ADP, ACMP, AECP_AEM

"""

AVDECC Controller Class

"""

class AVDECC_Controller():
    def __init__(self, _ethDev, _srcMAC):
        self.ethDev = _ethDev
        self.srcMAC = _srcMAC
        self.dstMAC = "91:e0:f0:01:00:00"
        self.ethType = 0x22f0
        self.ethFrame = Ether( src = self.srcMAC, dst = self.dstMAC, type = self.ethType )
        pass
    #----------------------------------------------------------------------------------------------------------------------------
    
    def sendADP_Announce(self):
        adp = ADP()
        discover = self.ethFrame / adp
        sendp( discover  , iface = self.ethDev)      
    #----------------------------------------------------------------------------------------------------------------------------  
        
    def connect_listener(self, streamId, destMac, talkerLocalId, talkerId, listenerLocalId, listenerId):
        acmp = ACMP()
        
        acmp.sv_avb_version_message_type = "CONNECT_TX_COMMAND"
        acmp.status = "SUCCESS"
        acmp.stream_id = streamId
        acmp.stream_dest_mac = destMac
        acmp.talker_id = talkerId
        acmp.talker_unique_id = talkerLocalId
        acmp.listener_id = listenerId
        acmp.listener_unique_id = listenerLocalId
                
        connect = self.ethFrame / acmp
        sendp( connect  , iface = self.ethDev)
        return 1
    #----------------------------------------------------------------------------------------------------------------------------
    
    def disconnect_listener(self, streamId, destMac):
        acmp = ACMP()
        
        acmp.sv_avb_version_message_type = "DISCONNECT_TX_COMMAND"
        acmp.status = "SUCCESS"
        acmp.stream_id = streamId
        acmp.stream_dest_mac = destMac
                
        connect = self.ethFrame / acmp
        sendp( connect  , iface = self.ethDev)
        return 1    
    #----------------------------------------------------------------------------------------------------------------------------

    def start_streaming(self, entity_id, controller_id, descriptor_type, descriptor_id):
        aecp = AECP_AEM()
        aem = AEM_START_STOP_STREAMING_CMD()
        
        aecp.sv_avb_version_message_type = "AEM_COMMAND"
        aecp.status = "SUCCESS"
        aecp.command_type = "START_STREAMING"
        aecp.entity_id= entity_id
        aecp.controller_id= controller_id
        aem.descriptor_type = descriptor_type
        aem.descriptor_id = descriptor_id
                
        start_streaming = self.ethFrame / aecp / aem
        sendp( start_streaming  , iface = self.ethDev)
        return 1   
    #----------------------------------------------------------------------------------------------------------------------------

    def stop_streaming(self, entity_id, controller_id, descriptor_type, descriptor_id):
        aecp = AECP_AEM()
        aem = AEM_START_STOP_STREAMING_CMD()
        
        aecp.sv_avb_version_message_type = "AEM_COMMAND"
        aecp.status = "SUCCESS"
        aecp.command_type = "STOP_STREAMING"
        aecp.entity_id= entity_id
        aecp.controller_id= controller_id
        aem.descriptor_type = descriptor_type
        aem.descriptor_id = descriptor_id
                
        start_streaming = self.ethFrame / aecp / aem
        sendp( start_streaming  , iface = self.ethDev)
        return 1  
    #----------------------------------------------------------------------------------------------------------------------------

    def set_stream_format(self, entity_id, controller_id, descriptor_type, descriptor_id):
        aecp = AECP_AEM()
        aem = AEM_SET_STREAM_FORMAT_CMD()
        avtp = AVTP_AUDIO_FORMAT()
        
        aecp.sv_avb_version_message_type = "AEM_COMMAND"
        aecp.status = "SUCCESS"
        aecp.command_type = "SET_STREAM_FORMAT"
        aecp.data_length_lo = 52
        aecp.entity_id= entity_id
        aecp.controller_id= controller_id
        aem.descriptor_type = descriptor_type
        aem.descriptor_id = descriptor_id
                
        start_streaming = self.ethFrame / aecp / aem / avtp
        sendp( start_streaming  , iface = self.ethDev)
        return 1   
    #----------------------------------------------------------------------------------------------------------------------------

    def get_stream_format(self, entity_id, controller_id, descriptor_type, descriptor_id):
        aecp = AECP_AEM()
        aem = AEM_GET_STREAM_FORAT_CMD()
        
        aecp.sv_avb_version_message_type = "AEM_COMMAND"
        aecp.status = "SUCCESS"
        aecp.command_type = "GET_STREAM_FORMAT"
        aecp.data_length_lo = 52
        aecp.entity_id= entity_id
        aecp.controller_id= controller_id
        aem.descriptor_type = descriptor_type
        aem.descriptor_id = descriptor_id
                
        start_streaming = self.ethFrame / aecp / aem
        sendp( start_streaming  , iface = self.ethDev)
        return 1  
    #----------------------------------------------------------------------------------------------------------------------------

    def set_control(self, entity_id, controller_id, descriptor_type, descriptor_id):
        aecp = AECP_AEM()
        
        aecp.sv_avb_version_message_type = "AEM_COMMAND"
        aecp.status = "SUCCESS"
        aecp.command_type = "SET_CONTROL"
        aecp.entity_id= entity_id
        aecp.controller_id= controller_id
        aecp.descriptor_type = descriptor_type
        aecp.descriptor_id = descriptor_id
                
        start_streaming = self.ethFrame / aecp
        sendp( start_streaming  , iface = self.ethDev)
        return 1   
    #----------------------------------------------------------------------------------------------------------------------------

    def get_control(self, entity_id, controller_id, descriptor_type, descriptor_id):
        aecp = AECP_AEM()
        
        aecp.sv_avb_version_message_type = "AEM_COMMAND"
        aecp.status = "SUCCESS"
        aecp.command_type = "GET_CONTROL"
        aecp.entity_id= entity_id
        aecp.controller_id= controller_id
        aecp.descriptor_type = descriptor_type
        aecp.descriptor_id = descriptor_id
                
        start_streaming = self.ethFrame / aecp
        sendp( start_streaming  , iface = self.ethDev)
        return 1  
    #----------------------------------------------------------------------------------------------------------------------------

    def control_increment(self, entity_id, controller_id, descriptor_type, descriptor_id):
        aecp = AECP_AEM()
        
        aecp.sv_avb_version_message_type = "AEM_COMMAND"
        aecp.status = "SUCCESS"
        aecp.command_type = "INCREMENT_CONTROL"
        aecp.entity_id= entity_id
        aecp.controller_id= controller_id
        aecp.descriptor_type = descriptor_type
        aecp.descriptor_id = descriptor_id
                
        start_streaming = self.ethFrame / aecp
        sendp( start_streaming  , iface = self.ethDev)
        return 1  
    #----------------------------------------------------------------------------------------------------------------------------

    def control_decrement(self, entity_id, controller_id, descriptor_type, descriptor_id):
        aecp = AECP_AEM()
        
        aecp.sv_avb_version_message_type = "AEM_COMMAND"
        aecp.status = "SUCCESS"
        aecp.command_type = "DECREMENT_CONTROL"
        aecp.entity_id= entity_id
        aecp.controller_id= controller_id
        aecp.descriptor_type = descriptor_type
        aecp.descriptor_id = descriptor_id
                
        start_streaming = self.ethFrame / aecp
        sendp( start_streaming  , iface = self.ethDev)
        return 1  
    #----------------------------------------------------------------------------------------------------------------------------
    
    
    def get_counters(self, entity_id, controller_id, descriptor_type, descriptor_id):
        aecp = AECP_AEM()
        aem = AEM_GET_COUNTERS_CMD()
        
        aecp.sv_avb_version_message_type = "AEM_COMMAND"
        aecp.status = "SUCCESS"
        aecp.command_type = "GET_COUNTERS"
        aecp.entity_id= entity_id
        aecp.controller_id= controller_id
        aem.descriptor_type = descriptor_type
        aem.descriptor_id = descriptor_id
                
        start_streaming = self.ethFrame / aecp / aem
        sendp( start_streaming  , iface = self.ethDev)
        return 1    
    #----------------------------------------------------------------------------------------------------------------------------







    def aecp_VENDOR_PAYLOAD_IPv4_Payload(self, entity_id, controller_id, command, target, port, ipv4_address):
        aecp = AECP_VENDOR()
                
        aecp.sv_avb_version_message_type = "VENDOR_UNIQUE_COMMAND"
        aecp.status = "SUCCESS"
        aecp.entity_id= entity_id
        aecp.controller_id= controller_id

        aecp_cmd = AECP_VENDOR_CMD_RESP()
        aecp_cmd.command = command#"V_CREATE"
        aecp_cmd.target = target#"V_TALKER"
        aecp_cmd.udp_payload_size = 256

        v_payload = VENDOR_PAYLOAD_IPv4()
        v_payload.udp_port = port#50000
        v_payload.ipv4_address0 = ipv4_address[0]
        v_payload.ipv4_address1 = ipv4_address[1]
        v_payload.ipv4_address2 = ipv4_address[2]
        v_payload.ipv4_address3 = ipv4_address[3]
                
        ipv4socket = self.ethFrame / aecp / aecp_cmd / v_payload
        sendp( ipv4socket  , iface = self.ethDev)
        return 1
    #----------------------------------------------------------------------------------------------------------------------------



    def aecp_VENDOR_PAYLOAD_QUIT(self, entity_id, controller_id, command):
        aecp = AECP_VENDOR()
                
        aecp.sv_avb_version_message_type = "VENDOR_UNIQUE_COMMAND"
        aecp.status = "SUCCESS"
        aecp.entity_id= entity_id
        aecp.controller_id= controller_id

        aecp_cmd = AECP_VENDOR_CMD_RESP()
        aecp_cmd.command = command#"V_CREATE"

                
        ipv4socket = self.ethFrame / aecp / aecp_cmd
        sendp( ipv4socket  , iface = self.ethDev)
        return 1
    #----------------------------------------------------------------------------------------------------------------------------





    def aecp_VENDOR_PAYLOAD_IPv6_Payload(self, entity_id, controller_id, command, target, port, ipv6_address):
        aecp = AECP_VENDOR()
                
        aecp.sv_avb_version_message_type = "VENDOR_UNIQUE_COMMAND"
        aecp.status = "SUCCESS"
        aecp.entity_id= entity_id
        aecp.controller_id= controller_id

        aecp_cmd = AECP_VENDOR_CMD_RESP()
        aecp_cmd.command = command#"V_CREATE"
        aecp_cmd.target = target#"V_TALKER"
        aecp_cmd.udp_payload_size = 256

        v_payload = VENDOR_PAYLOAD_IPv6()
        v_payload.udp_port = port#
        v_payload.ipv6_address0 = ipv6_address[0]
        v_payload.ipv6_address1 = ipv6_address[1]
        v_payload.ipv6_address2 = ipv6_address[2]
        v_payload.ipv6_address3 = ipv6_address[3]
        v_payload.ipv6_address4 = ipv6_address[4]
        v_payload.ipv6_address5 = ipv6_address[5]
        v_payload.ipv6_address6 = ipv6_address[6]
        v_payload.ipv6_address7 = ipv6_address[7]
                
        ipv4socket = self.ethFrame / aecp / aecp_cmd / v_payload
        sendp( ipv4socket  , iface = self.ethDev)
        return 1 
    #----------------------------------------------------------------------------------------------------------------------------


    def aecp_VENDOR_PAYLOAD_ID64BIT(self, entity_id, controller_id, command, target, endstation_id, payloadSize):
        aecp = AECP_VENDOR()
                
        aecp.sv_avb_version_message_type = "VENDOR_UNIQUE_COMMAND"
        aecp.status = "SUCCESS"
        aecp.entity_id= entity_id
        aecp.controller_id= controller_id

        aecp_cmd = AECP_VENDOR_CMD_RESP()
        aecp_cmd.command = command#"V_CREATE"
        aecp_cmd.target = target#"V_TALKER"
        aecp_cmd.udp_payload_size = payloadSize

        v_payload = VENDOR_PAYLOAD_ID64BIT()
        v_payload.endstation_id = endstation_id
                
        ipv4socket = self.ethFrame / aecp / aecp_cmd / v_payload
        sendp( ipv4socket  , iface = self.ethDev)
        return 1 
    #----------------------------------------------------------------------------------------------------------------------------
    
#==========================================================================================================================================
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
#     avdecc_ctl = AVDECC_Controller("enp3s0", "ac:9e:17:4e:7e:41")
    avdecc_ctl = AVDECC_Controller("enp2s0", "d8:cb:8a:32:28:1b")
    avdecc_ctl.sendADP_Announce()
    
    for i in range(0,2):
        avdecc_ctl.aecp_VENDOR_PAYLOAD_IPv4_Payload(0x0101010101010101+i, 
                                                    0x0101010101010101+i, 
                                                    "V_CREATE", "V_TALKER", 
                                                    50000+i, [223,144,83,i])
        avdecc_ctl.aecp_VENDOR_PAYLOAD_IPv4_Payload(0x0101010101010101+i, 
                                                    0x0101010101010101+i, 
                                                    "V_CREATE", "V_LISTENER", 
                                                    50000+i, [223,144,83,i])
        
    time.sleep(5)
    for i in range(0,2):
        avdecc_ctl.connect_listener(0x0101010101010101+i, "c3:51:00:00:01:00:03:01", i, 0x0101010101010101+i, i,0x0101010101010101+i,)
        
        
    time.sleep(20)
    avdecc_ctl.aecp_VENDOR_PAYLOAD_QUIT(0x0101010101010101, 0x0101010101010101, "V_QUIT")
    
    
#         avdecc_ctl.aecp_VENDOR_PAYLOAD_IPv6_Payload(0x0101010101010101+i, 
#                                                     0x0101010101010101+i, 
#                                                     "V_CREATE", "V_TALKER", 
#                                                     50000+i,  [
#                                                               0x1234,
#                                                               0x5678,
#                                                               0x1357,
#                                                               0x9753,
#                                                               0x2468,
#                                                               0x8642,
#                                                               0xabcd,
#                                                               i                                                                                                                              
#                                                               ])
#         avdecc_ctl.aecp_VENDOR_PAYLOAD_IPv6_Payload(0x0101010101010101+i, 
#                                                     0x0101010101010101+i, 
#                                                     "V_CREATE", "V_LISTENER", 
#                                                     50000+i, [
#                                                               0x1234,
#                                                               0x5678,
#                                                               0x1357,
#                                                               0x9753,
#                                                               0x2468,
#                                                               0x8642,
#                                                               0xabcd,
#                                                               i                                                                                                                              
#                                                               ])
#      
#      
#         avdecc_ctl.aecp_VENDOR_PAYLOAD_ID64BIT(0x0101010101010101+i, 
#                                                     0x0101010101010101+i, 
#                                                     "V_MODIFY", "V_LISTENER", 
#                                                     0x0101010101010101+i, 
#                                                     512 
#                                                     )
#         avdecc_ctl.aecp_VENDOR_PAYLOAD_ID64BIT(0x0101010101010101+i, 
#                                                     0x0101010101010101+i, 
#                                                     "V_MODIFY", "V_TALKER", 
#                                                     0x0101010101010101+i, 
#                                                     512 
#                                                     )
#          
#          
#          
#          
#      
#      
#      
#     for i in range(0,8):
#         avdecc_ctl.start_streaming(0x0101010101010101, 0x0101010101010101, "STREAM_INPUT_TYPE", i)
#         avdecc_ctl.start_streaming(0x0101010101010101, 0x0101010101010101, "STREAM_OUTPUT_TYPE", i)
#          
#          
#          
#     avdecc_ctl.get_stream_format(0x0101010101010101, 0x0101010101010101, "STREAM_INPUT_TYPE", 5)
#     avdecc_ctl.set_stream_format(0x0101010101010101, 0x0101010101010101, "STREAM_INPUT_TYPE", 5)
#     avdecc_ctl.get_counters(0x0101010101010101, 0x0101010101010101, "ENTITY_TYPE", 5)
#     avdecc_ctl.get_counters(0x0101010101010101, 0x0101010101010101, "AVB_INTERFACE_TYPE", 5)
#     avdecc_ctl.get_counters(0x0101010101010101, 0x0101010101010101, "STREAM_INPUT_TYPE", 5)
#     avdecc_ctl.get_counters(0x0101010101010101, 0x0101010101010101, "CLOCK_SOURCE_TYPE", 5)
#          
#     for i in range(0,8):
#         avdecc_ctl.stop_streaming(0x0101010101010101, 0x0101010101010101, "STREAM_INPUT_TYPE", i)
#         avdecc_ctl.stop_streaming(0x0101010101010101, 0x0101010101010101, "STREAM_OUTPUT_TYPE", i)
#      
#      
#      
#      
#     for i in range(0,8):
#         avdecc_ctl.disconnect_listener(0x0101010101010101+i, "c3:51:00:00:01:00:03:01")
#          
#         avdecc_ctl.aecp_VENDOR_PAYLOAD_IPv4_Payload(0x0101010101010101+i, 
#                                                     0x0101010101010101+i, 
#                                                     "V_DESTROY", "V_TALKER", 
#                                                     50000+i, [223,144,83,i])
#         avdecc_ctl.aecp_VENDOR_PAYLOAD_IPv4_Payload(0x0101010101010101+i, 
#                                                     0x0101010101010101+i, 
#                                                     "V_DESTROY", "V_LISTENER", 
#                                                     50000+i, [223,144,83,i])
#         avdecc_ctl.aecp_VENDOR_PAYLOAD_IPv6_Payload(0x0101010101010101+i, 
#                                                     0x0101010101010101+i, 
#                                                     "V_DESTROY", "V_TALKER", 
#                                                     50000+i,  [
#                                                               0x1234,
#                                                               0x5678,
#                                                               0x1357,
#                                                               0x9753,
#                                                               0x2468,
#                                                               0x8642,
#                                                               0xabcd,
#                                                               i                                                                                                                              
#                                                               ])
#         avdecc_ctl.aecp_VENDOR_PAYLOAD_IPv6_Payload(0x0101010101010101+i, 
#                                                     0x0101010101010101+i, 
#                                                     "V_DESTROY", "V_LISTENER", 
#                                                     50000+i, [
#                                                               0x1234,
#                                                               0x5678,
#                                                               0x1357,
#                                                               0x9753,
#                                                               0x2468,
#                                                               0x8642,
#                                                               0xabcd,
#                                                               i                                                                                                                         
#                                                               ])
#     
#     
#     
#     
#     for idx in range(0,5):
#         pkts = sniff(filter="ether dst %s"%avdecc_ctl.dstMAC, iface = avdecc_ctl.ethDev, count=1)
#         
#         eth = Ether(pkts[0].__bytes__() )
#         print( eth.src )
#         print( eth.dst )
#         print( hex( eth.type ) )
#                            
#         adp = ADP( eth.payload.__bytes__() )
#         print( adp.mysummary() )
#         print( hex( adp.entity_id ) )
#         print( hex( adp.vendor_id ) )
#         print( hex( adp.model_id ) )
#         print( adp.entity_capabilities )
#         print( hex( adp.talker_stream_sources ) )
#         print( adp.talker_capabilities )
#         print( hex( adp.listener_stream_sinks ) )
#         print( hex( adp.listener_capabilites ) )
#         print( hex( adp.controller_capabilities ) )
#         print( hex( adp.available_index ) )
#         print( hex( adp.as_grandmaster_id ) )
#         print( hex( adp.default_audio_format ) )
#         print( hex( adp.default_video_format ) )
#         print( hex( adp.association_id ) )
#         print( hex( adp.entity_type ) )
