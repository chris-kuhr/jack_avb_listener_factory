'''
Created on Apr 19, 2017

@author: christoph
'''
from scapy.all import *

class DestMACField(MACField):
    def __init__(self, name):
        MACField.__init__(self, name, None)
    def i2h(self, pkt, x):
        if x is None:
            x = conf.neighbor.resolve(pkt,pkt.payload)
            if x is None:
                x = "ff:ff:ff:ff:ff:ff"
                warning("Mac address to reach destination not found. Using broadcast.")
        return MACField.i2h(self, pkt, x)
    def i2m(self, pkt, x):
        return MACField.i2m(self, pkt, self.i2h(pkt, x))
      
class ADP(Packet):
    name = "ADP_Packet "  
    fields_desc=[ ByteEnumField("cd_subtype",0xfa, {0xfa: "ADP"}) ,
                 ByteEnumField("sv_avb_version_msg_type",0x00,{
                                                                0: "ENTITY_AVAILABLE",
                                                                1: "ENTITY_DEPARTING",
                                                                2: "ENTITY_DISCOVER"
                                                            }) ,
                 XByteField("valid_time_data_length_hi",0x00) ,
                 XByteField("data_length_lo",0x34),
                 
                 XLongField("entity_id",0xfedcba9876543210) ,
                 XIntField("vendor_id",0x76543210) ,
                 XIntField("model_id",0x76543210) ,
                 IntEnumField("entity_capabilities",0x76543210, {
                                                                    0x00000001: "ENTITY_CAPABILITIES_AVDECC_IP",
                                                                    0x00000002: "ENTITY_CAPABILITIES_ZERO_CONF",
                                                                    0x00000004: "ENTITY_CAPABILITIES_GATEWAY_ENTITY",
                                                                    0x00000008: "ENTITY_CAPABILITIES_AVDECC_CONTROL",
                                                                    0x00000010: "ENTITY_CAPABILITIES_LEGACY_AVC",
                                                                    0x00000020: "ENTITY_CAPIBILITIES_ASSOCIATION_ID_SUPPORTED",
                                                                    0x00000040: "ENTITY_CAPIBILITIES_ASSOCIATION_ID_VALID"
                                                                 }) ,
                 XShortField("talker_stream_sources",0x3210) ,
                 ShortEnumField("talker_capabilities",0x3210, {
                                                                    0x0001: "TALKER_CAPABILITIES_IMPLEMENTED",
                                                                    0x0200: "TALKER_CAPABILITIES_OTHER_SOURCE",
                                                                    0x0400: "TALKER_CAPABILITIES_CONTROL_SOURCE",
                                                                    0x0800: "TALKER_CAPABILITIES_MEDIA_CLOCK_SOURCE",
                                                                    0x1000: "TALKER_CAPABILITIES_SMPTE_SOURCE",
                                                                    0x2000: "TALKER_CAPABILITIES_MIDI_SOURCE",
                                                                    0x4000: "TALKER_CAPABILITIES_AUDIO_SOURCE",
                                                                    0x8000: "TALKER_CAPABILITIES_VIDEO_SOURCE"
                                                           }) ,
                 XShortField("listener_stream_sinks",0x3210) ,
                 ShortEnumField("listener_capabilites",0x3210, {
                                                                    0x0001: "LISTENER_CAPABILITIES_IMPLEMENTED",
                                                                    0x0200: "LISTENER_CAPABILITIES_OTHER_SINK",
                                                                    0x0400: "LISTENER_CAPABILITIES_CONTROL_SINK",
                                                                    0x0800: "LISTENER_CAPABILITIES_MEDIA_CLOCK_SINK",
                                                                    0x1000: "LISTENER_CAPABILITIES_SMPTE_SINK",
                                                                    0x2000: "LISTENER_CAPABILITIES_MIDI_SINK",
                                                                    0x4000: "LISTENER_CAPABILITIES_AUDIO_SINK",
                                                                    0x8000: "LISTENER_CAPABILITIES_VIDEO_SINK"
                                                            }) ,
                 IntEnumField("controller_capabilities",0x76543210, {
                                                                    0x00000001: "CONTROLLER_CAPABILITIES_IMPLEMENTED",
                                                                    0x00000002: "CONTROLLER_CAPABILITIES_LAYER3_PROXY"
                                                                 }) ,
                 XIntField("available_index",0x76543210) ,
                 XLongField("as_grandmaster_id",0xfedcba9876543210) ,
                 IntEnumField("default_audio_format",0x76543210, {
                                                                    0xFC000000: "DEFAULT_AUDIO_SAMPLE_RATES_MASK",
                                                                    0x03FC0000: "DEFAULT_AUDIO_MAX_CHANS_MASK",
                                                                    0x00020000: "DEFAULT_AUDIO_SAF_MASK",
                                                                    0x00010000: "DEFAULT_AUDIO_FLOAT_MASK ",
                                                                    0x0000FFFF: "DEFAULT_AUDIO_CHAN_FORMATS_MASK",
                                                                    0x00000001: "DEFAULT_AUDIO_FORMAT_MONO",
                                                                    0x00000002: "DEFAULT_AUDIO_FORMAT_2_CH",
                                                                    0x00000004: "DEFAULT_AUDIO_FORMAT_3_CH",
                                                                    0x00000008: "DEFAULT_AUDIO_FORMAT_4_CH",
                                                                    0x00000010: "DEFAULT_AUDIO_FORMAT_5_CH",
                                                                    0x00000020: "DEFAULT_AUDIO_FORMAT_6_CH",
                                                                    0x00000040: "DEFAULT_AUDIO_FORMAT_7_CH",
                                                                    0x00000080: "DEFAULT_AUDIO_FORMAT_8_CH",
                                                                    0x00000100: "DEFAULT_AUDIO_FORMAT_10_CH",
                                                                    0x00000200: "DEFAULT_AUDIO_FORMAT_12_CH",
                                                                    0x00000400: "DEFAULT_AUDIO_FORMAT_14_CH",
                                                                    0x00000800: "DEFAULT_AUDIO_FORMAT_16_CH",
                                                                    0x00001000: "DEFAULT_AUDIO_FORMAT_18_CH",
                                                                    0x00002000: "DEFAULT_AUDIO_FORMAT_20_CH",
                                                                    0x00004000: "DEFAULT_AUDIO_FORMAT_22_CH",
                                                                    0x00008000: "DEFAULT_AUDIO_FORMAT_24_CH",
                                                                    0x00010000: "DEFAULT_AUDIO_FORMAT_FLOAT",
                                                                    0x00020000: "DEFAULT_AUDIO_FORMAT_SAF",
                                                                    0x00100000: "DEFAULT_AUDIO_FORMAT_MAX_STREAMS_4",
                                                                    0x00200000: "DEFAULT_AUDIO_FORMAT_MAX_STREAMS_8",
                                                                    0x00400000: "DEFAULT_AUDIO_FORMAT_MAX_STREAMS_16",
                                                                    0x04000000: "DEFAULT_AUDIO_FORMAT_44K1",
                                                                    0x08000000: "DEFAULT_AUDIO_FORMAT_48K",
                                                                    0x10000000: "DEFAULT_AUDIO_FORMAT_88K2",
                                                                    0x20000000: "DEFAULT_AUDIO_FORMAT_96K",
                                                                    0x40000000: "DEFAULT_AUDIO_FORMAT_176K4",
                                                                    0x80000000: "DEFAULT_AUDIO_FORMAT_192K"
                                                              }) ,
                 IntEnumField("default_video_format",0x76543210, {0: "DEFAULT_VIDEO_FORMAT"
                                                              }) ,
                 XLongField("association_id",0xfedcba9876543210) ,
                 IntEnumField("entity_type",0x76543210, {
                                                                    0x00000001: "ENTITY_TYPE_OTHER",
                                                                    0x00000002: "ENTITY_TYPE_MULTIFUNCTION",
                                                                    0x00000004: "ENTITY_TYPE_LOUDSPEAKER",
                                                                    0x00000008: "ENTITY_TYPE_MICROPHONE",
                                                                    0x00000010: "ENTITY_TYPE_AUDIO_AMPLIFIER",
                                                                    0x00000020: "ENTITY_TYPE_AUDIO_SOURCE",
                                                                    0x00000040: "ENTITY_TYPE_AUDIO_PROCESSOR",
                                                                    0x00000080: "ENTITY_TYPE_AUDIO_MIXER",
                                                                    0x00000100: "ENTITY_TYPE_HEADSET",
                                                                    0x00000200: "ENTITY_TYPE_COMPUTER",
                                                                    0x00000400: "ENTITY_TYPE_MUSICAL_INSTRUMENT",
                                                                    0x00000800: "ENTITY_TYPE_MIDI_DEVICE",
                                                                    0x00001000: "ENTITY_TYPE_MEDIA_SERVER",
                                                                    0x00002000: "ENTITY_TYPE_MEDIA_RECORDER",
                                                                    0x00004000: "ENTITY_TYPE_VIDEO_SOURCE",
                                                                    0x00008000: "ENTITY_TYPE_VIDEO_DISPLAY",
                                                                    0x00010000: "ENTITY_TYPE_VIDEO_PROCESSOR",
                                                                    0x00020000: "ENTITY_TYPE_VIDEO_MIXER",
                                                                    0x00040000: "ENTITY_TYPE_TIMING_DEVICE"
                                                     })  ]
    def mysummary(self):
        return self.sprintf("cd_subtype %cd_subtype%\n\
sv_avb_version_msg_type %sv_avb_version_msg_type%\n\
valid_time_data_length_hi %valid_time_data_length_hi%\n\
data_length_lo %data_length_lo%\n\
entity_id %entity_id%\n\
vendor_id %vendor_id%\n\
model_id %model_id%\n\
entity_capabilities %entity_capabilities%\n\
talker_stream_sources %talker_stream_sources%\n\
talker_capabilities %talker_capabilities%\n\
listener_stream_sinks %listener_stream_sinks%\n\
listener_capabilites %listener_capabilites%\n\
controller_capabilities %controller_capabilities%\n\
available_index %available_index%\n\
as_grandmaster_id %as_grandmaster_id%\n\
default_audio_format %default_audio_format%\n\
default_video_format %default_video_format%\n\
association_id %association_id%\n\
entity_type %entity_type%")
    
    
    
    
    
                 
    """
    AEM COMMANDS
    """
    
class AEM_READ_DESCRIPTOR_CMD(Packet):
    name = "AEM_READ_DESCRIPTOR_CMD_Payload "  
    fields_desc=[ ShortEnumField("descriptor_type",0x3210,{                                                          
                                            0x0000: "ENTITY_TYPE" ,                
                                            0x0001: "CONFIGURATION_TYPE",          
                                            0x0002: "AUDIO_UNIT_TYPE",             
                                            0x0003: "VIDEO_UNIT_TYPE",             
                                            0x0004: "SENDOR_UNIT_TYPE",            
                                            0x0005: "STREAM_INPUT_TYPE",           
                                            0x0006: "STREAM_OUTPUT_TYPE",          
                                            0x0007: "JACK_INPUT_TYPE",             
                                            0x0008: "JACK_OUTPUT_TYPE",            
                                            0x0009: "AVB_INTERFACE_TYPE",          
                                            0x000a: "CLOCK_SOURCE_TYPE",           
                                            0x000b: "MEMORY_OBJECT_TYPE",          
                                            0x000c: "LOCALE_TYPE",                 
                                            0x000d: "STRINGS_TYPE",                
                                            0x000e: "STREAM_PORT_INPUT_TYPE",      
                                            0x000f: "STREAM_PORT_OUTPUT_TYPE",     
                                            0x0010: "EXTERNAL_PORT_INPUT_TYPE",    
                                            0x0011: "EXTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0012: "INTERNAL_PORT_INPUT_TYPE",    
                                            0x0013: "INTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0014: "AUDIO_CLUSTER_TYPE",          
                                            0x0015: "VIDEO_CLUSTER_TYPE",          
                                            0x0016: "SENSOR_CLUSTER_TYPE",         
                                            0x0017: "AUDIO_MAP_TYPE",              
                                            0x0018: "VIDEO_MAP_TYPE",              
                                            0x0019: "SENSOR_MAP_TYPE",             
                                            0x001a: "CONTROL_TYPE",                
                                            0x001b: "SIGNAL_SELECTOR_TYPE",        
                                            0x001c: "MIXER_TYPE",                  
                                            0x001d: "MATRIX_TYPE",                 
                                            0x001e: "MATRIX_SIGNAL_TYPE",          
                                            0x001f: "SIGNAL_SPLITTER_TYPE",        
                                            0x0020: "SIGNAL_COMBINER_TYPE",        
                                            0x0021: "SIGNAL_DEMULTIPLEXER_TYPE",    
                                            0x0022: "SIGNAL_MULTIPLEXER_TYPE",        
                                            0x0023: "SIGNAL_TRANSCODER_TYPE",        
                                            0x0024: "CLOCK_DOMAIN_TYPE",            
                                            0x0025: "CONTROL_BLOCK_TYPE",            
                                            0xffff: "INVALID_TYPE"               
                                                          })  ,                 
                 XShortField("descriptor_id",0x3210)   ]
           
class AEM_READ_DESCRIPTOR_RESP(Packet):
    name = "AEM_READ_DESCRIPTOR_RESP_Payload "  
    fields_desc=[ ShortEnumField("descriptor_type",0x3210,{                                                          
                                            0x0000: "ENTITY_TYPE" ,                
                                            0x0001: "CONFIGURATION_TYPE",          
                                            0x0002: "AUDIO_UNIT_TYPE",             
                                            0x0003: "VIDEO_UNIT_TYPE",             
                                            0x0004: "SENDOR_UNIT_TYPE",            
                                            0x0005: "STREAM_INPUT_TYPE",           
                                            0x0006: "STREAM_OUTPUT_TYPE",          
                                            0x0007: "JACK_INPUT_TYPE",             
                                            0x0008: "JACK_OUTPUT_TYPE",            
                                            0x0009: "AVB_INTERFACE_TYPE",          
                                            0x000a: "CLOCK_SOURCE_TYPE",           
                                            0x000b: "MEMORY_OBJECT_TYPE",          
                                            0x000c: "LOCALE_TYPE",                 
                                            0x000d: "STRINGS_TYPE",                
                                            0x000e: "STREAM_PORT_INPUT_TYPE",      
                                            0x000f: "STREAM_PORT_OUTPUT_TYPE",     
                                            0x0010: "EXTERNAL_PORT_INPUT_TYPE",    
                                            0x0011: "EXTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0012: "INTERNAL_PORT_INPUT_TYPE",    
                                            0x0013: "INTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0014: "AUDIO_CLUSTER_TYPE",          
                                            0x0015: "VIDEO_CLUSTER_TYPE",          
                                            0x0016: "SENSOR_CLUSTER_TYPE",         
                                            0x0017: "AUDIO_MAP_TYPE",              
                                            0x0018: "VIDEO_MAP_TYPE",              
                                            0x0019: "SENSOR_MAP_TYPE",             
                                            0x001a: "CONTROL_TYPE",                
                                            0x001b: "SIGNAL_SELECTOR_TYPE",        
                                            0x001c: "MIXER_TYPE",                  
                                            0x001d: "MATRIX_TYPE",                 
                                            0x001e: "MATRIX_SIGNAL_TYPE",          
                                            0x001f: "SIGNAL_SPLITTER_TYPE",        
                                            0x0020: "SIGNAL_COMBINER_TYPE",        
                                            0x0021: "SIGNAL_DEMULTIPLEXER_TYPE",    
                                            0x0022: "SIGNAL_MULTIPLEXER_TYPE",        
                                            0x0023: "SIGNAL_TRANSCODER_TYPE",        
                                            0x0024: "CLOCK_DOMAIN_TYPE",            
                                            0x0025: "CONTROL_BLOCK_TYPE",            
                                            0xffff: "INVALID_TYPE"               
                                                          })  ,                 
                 XShortField("descriptor_id",0x3210)   ]
           
class AEM_ACQUIRE_ENTITY_CMD(Packet):
    name = "AEM_ACQUIRE_ENTITY_CMD_Payload "  
    fields_desc=[ ShortEnumField("descriptor_type",0x3210,{                                                          
                                            0x0000: "ENTITY_TYPE" ,                
                                            0x0001: "CONFIGURATION_TYPE",          
                                            0x0002: "AUDIO_UNIT_TYPE",             
                                            0x0003: "VIDEO_UNIT_TYPE",             
                                            0x0004: "SENDOR_UNIT_TYPE",            
                                            0x0005: "STREAM_INPUT_TYPE",           
                                            0x0006: "STREAM_OUTPUT_TYPE",          
                                            0x0007: "JACK_INPUT_TYPE",             
                                            0x0008: "JACK_OUTPUT_TYPE",            
                                            0x0009: "AVB_INTERFACE_TYPE",          
                                            0x000a: "CLOCK_SOURCE_TYPE",           
                                            0x000b: "MEMORY_OBJECT_TYPE",          
                                            0x000c: "LOCALE_TYPE",                 
                                            0x000d: "STRINGS_TYPE",                
                                            0x000e: "STREAM_PORT_INPUT_TYPE",      
                                            0x000f: "STREAM_PORT_OUTPUT_TYPE",     
                                            0x0010: "EXTERNAL_PORT_INPUT_TYPE",    
                                            0x0011: "EXTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0012: "INTERNAL_PORT_INPUT_TYPE",    
                                            0x0013: "INTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0014: "AUDIO_CLUSTER_TYPE",          
                                            0x0015: "VIDEO_CLUSTER_TYPE",          
                                            0x0016: "SENSOR_CLUSTER_TYPE",         
                                            0x0017: "AUDIO_MAP_TYPE",              
                                            0x0018: "VIDEO_MAP_TYPE",              
                                            0x0019: "SENSOR_MAP_TYPE",             
                                            0x001a: "CONTROL_TYPE",                
                                            0x001b: "SIGNAL_SELECTOR_TYPE",        
                                            0x001c: "MIXER_TYPE",                  
                                            0x001d: "MATRIX_TYPE",                 
                                            0x001e: "MATRIX_SIGNAL_TYPE",          
                                            0x001f: "SIGNAL_SPLITTER_TYPE",        
                                            0x0020: "SIGNAL_COMBINER_TYPE",        
                                            0x0021: "SIGNAL_DEMULTIPLEXER_TYPE",    
                                            0x0022: "SIGNAL_MULTIPLEXER_TYPE",        
                                            0x0023: "SIGNAL_TRANSCODER_TYPE",        
                                            0x0024: "CLOCK_DOMAIN_TYPE",            
                                            0x0025: "CONTROL_BLOCK_TYPE",            
                                            0xffff: "INVALID_TYPE"               
                                                          })  ,                 
                 XShortField("descriptor_id",0x3210)   ]
    
class AEM_GET_AVB_INFO_CMD(Packet):
    name = "AEM_GET_AVB_INFO_CMD_Payload "  
    fields_desc=[ ShortEnumField("descriptor_type",0x3210,{                                                          
                                            0x0000: "ENTITY_TYPE" ,                
                                            0x0001: "CONFIGURATION_TYPE",          
                                            0x0002: "AUDIO_UNIT_TYPE",             
                                            0x0003: "VIDEO_UNIT_TYPE",             
                                            0x0004: "SENDOR_UNIT_TYPE",            
                                            0x0005: "STREAM_INPUT_TYPE",           
                                            0x0006: "STREAM_OUTPUT_TYPE",          
                                            0x0007: "JACK_INPUT_TYPE",             
                                            0x0008: "JACK_OUTPUT_TYPE",            
                                            0x0009: "AVB_INTERFACE_TYPE",          
                                            0x000a: "CLOCK_SOURCE_TYPE",           
                                            0x000b: "MEMORY_OBJECT_TYPE",          
                                            0x000c: "LOCALE_TYPE",                 
                                            0x000d: "STRINGS_TYPE",                
                                            0x000e: "STREAM_PORT_INPUT_TYPE",      
                                            0x000f: "STREAM_PORT_OUTPUT_TYPE",     
                                            0x0010: "EXTERNAL_PORT_INPUT_TYPE",    
                                            0x0011: "EXTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0012: "INTERNAL_PORT_INPUT_TYPE",    
                                            0x0013: "INTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0014: "AUDIO_CLUSTER_TYPE",          
                                            0x0015: "VIDEO_CLUSTER_TYPE",          
                                            0x0016: "SENSOR_CLUSTER_TYPE",         
                                            0x0017: "AUDIO_MAP_TYPE",              
                                            0x0018: "VIDEO_MAP_TYPE",              
                                            0x0019: "SENSOR_MAP_TYPE",             
                                            0x001a: "CONTROL_TYPE",                
                                            0x001b: "SIGNAL_SELECTOR_TYPE",        
                                            0x001c: "MIXER_TYPE",                  
                                            0x001d: "MATRIX_TYPE",                 
                                            0x001e: "MATRIX_SIGNAL_TYPE",          
                                            0x001f: "SIGNAL_SPLITTER_TYPE",        
                                            0x0020: "SIGNAL_COMBINER_TYPE",        
                                            0x0021: "SIGNAL_DEMULTIPLEXER_TYPE",    
                                            0x0022: "SIGNAL_MULTIPLEXER_TYPE",        
                                            0x0023: "SIGNAL_TRANSCODER_TYPE",        
                                            0x0024: "CLOCK_DOMAIN_TYPE",            
                                            0x0025: "CONTROL_BLOCK_TYPE",            
                                            0xffff: "INVALID_TYPE"               
                                                          })  ,                 
                 XShortField("descriptor_id",0x3210)   ]
    
class AEM_GET_AVB_INFO_RESP(Packet):
    name = "AEM_GET_AVB_INFO_RESP_Payload "  
    fields_desc=[ ShortEnumField("descriptor_type",0x3210,{                                                          
                                            0x0000: "ENTITY_TYPE" ,                
                                            0x0001: "CONFIGURATION_TYPE",          
                                            0x0002: "AUDIO_UNIT_TYPE",             
                                            0x0003: "VIDEO_UNIT_TYPE",             
                                            0x0004: "SENDOR_UNIT_TYPE",            
                                            0x0005: "STREAM_INPUT_TYPE",           
                                            0x0006: "STREAM_OUTPUT_TYPE",          
                                            0x0007: "JACK_INPUT_TYPE",             
                                            0x0008: "JACK_OUTPUT_TYPE",            
                                            0x0009: "AVB_INTERFACE_TYPE",          
                                            0x000a: "CLOCK_SOURCE_TYPE",           
                                            0x000b: "MEMORY_OBJECT_TYPE",          
                                            0x000c: "LOCALE_TYPE",                 
                                            0x000d: "STRINGS_TYPE",                
                                            0x000e: "STREAM_PORT_INPUT_TYPE",      
                                            0x000f: "STREAM_PORT_OUTPUT_TYPE",     
                                            0x0010: "EXTERNAL_PORT_INPUT_TYPE",    
                                            0x0011: "EXTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0012: "INTERNAL_PORT_INPUT_TYPE",    
                                            0x0013: "INTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0014: "AUDIO_CLUSTER_TYPE",          
                                            0x0015: "VIDEO_CLUSTER_TYPE",          
                                            0x0016: "SENSOR_CLUSTER_TYPE",         
                                            0x0017: "AUDIO_MAP_TYPE",              
                                            0x0018: "VIDEO_MAP_TYPE",              
                                            0x0019: "SENSOR_MAP_TYPE",             
                                            0x001a: "CONTROL_TYPE",                
                                            0x001b: "SIGNAL_SELECTOR_TYPE",        
                                            0x001c: "MIXER_TYPE",                  
                                            0x001d: "MATRIX_TYPE",                 
                                            0x001e: "MATRIX_SIGNAL_TYPE",          
                                            0x001f: "SIGNAL_SPLITTER_TYPE",        
                                            0x0020: "SIGNAL_COMBINER_TYPE",        
                                            0x0021: "SIGNAL_DEMULTIPLEXER_TYPE",    
                                            0x0022: "SIGNAL_MULTIPLEXER_TYPE",        
                                            0x0023: "SIGNAL_TRANSCODER_TYPE",        
                                            0x0024: "CLOCK_DOMAIN_TYPE",            
                                            0x0025: "CONTROL_BLOCK_TYPE",            
                                            0xffff: "INVALID_TYPE"               
                                                          })  ,                 
                 XShortField("descriptor_id",0x3210)   ]
       
class AEM_LOCK_ENTITY_CMD(Packet):
    name = "AEM_LOCK_ENTITY_CMD_Payload "  
    fields_desc=[ ShortEnumField("descriptor_type",0x3210,{                                                          
                                            0x0000: "ENTITY_TYPE" ,                
                                            0x0001: "CONFIGURATION_TYPE",          
                                            0x0002: "AUDIO_UNIT_TYPE",             
                                            0x0003: "VIDEO_UNIT_TYPE",             
                                            0x0004: "SENDOR_UNIT_TYPE",            
                                            0x0005: "STREAM_INPUT_TYPE",           
                                            0x0006: "STREAM_OUTPUT_TYPE",          
                                            0x0007: "JACK_INPUT_TYPE",             
                                            0x0008: "JACK_OUTPUT_TYPE",            
                                            0x0009: "AVB_INTERFACE_TYPE",          
                                            0x000a: "CLOCK_SOURCE_TYPE",           
                                            0x000b: "MEMORY_OBJECT_TYPE",          
                                            0x000c: "LOCALE_TYPE",                 
                                            0x000d: "STRINGS_TYPE",                
                                            0x000e: "STREAM_PORT_INPUT_TYPE",      
                                            0x000f: "STREAM_PORT_OUTPUT_TYPE",     
                                            0x0010: "EXTERNAL_PORT_INPUT_TYPE",    
                                            0x0011: "EXTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0012: "INTERNAL_PORT_INPUT_TYPE",    
                                            0x0013: "INTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0014: "AUDIO_CLUSTER_TYPE",          
                                            0x0015: "VIDEO_CLUSTER_TYPE",          
                                            0x0016: "SENSOR_CLUSTER_TYPE",         
                                            0x0017: "AUDIO_MAP_TYPE",              
                                            0x0018: "VIDEO_MAP_TYPE",              
                                            0x0019: "SENSOR_MAP_TYPE",             
                                            0x001a: "CONTROL_TYPE",                
                                            0x001b: "SIGNAL_SELECTOR_TYPE",        
                                            0x001c: "MIXER_TYPE",                  
                                            0x001d: "MATRIX_TYPE",                 
                                            0x001e: "MATRIX_SIGNAL_TYPE",          
                                            0x001f: "SIGNAL_SPLITTER_TYPE",        
                                            0x0020: "SIGNAL_COMBINER_TYPE",        
                                            0x0021: "SIGNAL_DEMULTIPLEXER_TYPE",    
                                            0x0022: "SIGNAL_MULTIPLEXER_TYPE",        
                                            0x0023: "SIGNAL_TRANSCODER_TYPE",        
                                            0x0024: "CLOCK_DOMAIN_TYPE",            
                                            0x0025: "CONTROL_BLOCK_TYPE",            
                                            0xffff: "INVALID_TYPE"               
                                                          })  ,                 
                 XShortField("descriptor_id",0x3210)   ]
    
class AEM_START_STOP_STREAMING_CMD(Packet):
    name = "AEM_START_STOP_STREAMING_CMD_Payload "  
    fields_desc=[ ShortEnumField("descriptor_type",0x3210,{                                                          
                                            0x0000: "ENTITY_TYPE" ,                
                                            0x0001: "CONFIGURATION_TYPE",          
                                            0x0002: "AUDIO_UNIT_TYPE",             
                                            0x0003: "VIDEO_UNIT_TYPE",             
                                            0x0004: "SENDOR_UNIT_TYPE",            
                                            0x0005: "STREAM_INPUT_TYPE",           
                                            0x0006: "STREAM_OUTPUT_TYPE",          
                                            0x0007: "JACK_INPUT_TYPE",             
                                            0x0008: "JACK_OUTPUT_TYPE",            
                                            0x0009: "AVB_INTERFACE_TYPE",          
                                            0x000a: "CLOCK_SOURCE_TYPE",           
                                            0x000b: "MEMORY_OBJECT_TYPE",          
                                            0x000c: "LOCALE_TYPE",                 
                                            0x000d: "STRINGS_TYPE",                
                                            0x000e: "STREAM_PORT_INPUT_TYPE",      
                                            0x000f: "STREAM_PORT_OUTPUT_TYPE",     
                                            0x0010: "EXTERNAL_PORT_INPUT_TYPE",    
                                            0x0011: "EXTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0012: "INTERNAL_PORT_INPUT_TYPE",    
                                            0x0013: "INTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0014: "AUDIO_CLUSTER_TYPE",          
                                            0x0015: "VIDEO_CLUSTER_TYPE",          
                                            0x0016: "SENSOR_CLUSTER_TYPE",         
                                            0x0017: "AUDIO_MAP_TYPE",              
                                            0x0018: "VIDEO_MAP_TYPE",              
                                            0x0019: "SENSOR_MAP_TYPE",             
                                            0x001a: "CONTROL_TYPE",                
                                            0x001b: "SIGNAL_SELECTOR_TYPE",        
                                            0x001c: "MIXER_TYPE",                  
                                            0x001d: "MATRIX_TYPE",                 
                                            0x001e: "MATRIX_SIGNAL_TYPE",          
                                            0x001f: "SIGNAL_SPLITTER_TYPE",        
                                            0x0020: "SIGNAL_COMBINER_TYPE",        
                                            0x0021: "SIGNAL_DEMULTIPLEXER_TYPE",    
                                            0x0022: "SIGNAL_MULTIPLEXER_TYPE",        
                                            0x0023: "SIGNAL_TRANSCODER_TYPE",        
                                            0x0024: "CLOCK_DOMAIN_TYPE",            
                                            0x0025: "CONTROL_BLOCK_TYPE",            
                                            0xffff: "INVALID_TYPE"               
                                                          })  ,                 
                 XShortField("descriptor_id",0x3210)   ]
    
class AEM_GET_STREAM_FORAT_CMD(Packet):
    name = "AEM_GET_STREAM_FORAT_CMD_Payload "  
    fields_desc=[ ShortEnumField("descriptor_type",0x3210,{                                                          
                                            0x0000: "ENTITY_TYPE" ,                
                                            0x0001: "CONFIGURATION_TYPE",          
                                            0x0002: "AUDIO_UNIT_TYPE",             
                                            0x0003: "VIDEO_UNIT_TYPE",             
                                            0x0004: "SENDOR_UNIT_TYPE",            
                                            0x0005: "STREAM_INPUT_TYPE",           
                                            0x0006: "STREAM_OUTPUT_TYPE",          
                                            0x0007: "JACK_INPUT_TYPE",             
                                            0x0008: "JACK_OUTPUT_TYPE",            
                                            0x0009: "AVB_INTERFACE_TYPE",          
                                            0x000a: "CLOCK_SOURCE_TYPE",           
                                            0x000b: "MEMORY_OBJECT_TYPE",          
                                            0x000c: "LOCALE_TYPE",                 
                                            0x000d: "STRINGS_TYPE",                
                                            0x000e: "STREAM_PORT_INPUT_TYPE",      
                                            0x000f: "STREAM_PORT_OUTPUT_TYPE",     
                                            0x0010: "EXTERNAL_PORT_INPUT_TYPE",    
                                            0x0011: "EXTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0012: "INTERNAL_PORT_INPUT_TYPE",    
                                            0x0013: "INTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0014: "AUDIO_CLUSTER_TYPE",          
                                            0x0015: "VIDEO_CLUSTER_TYPE",          
                                            0x0016: "SENSOR_CLUSTER_TYPE",         
                                            0x0017: "AUDIO_MAP_TYPE",              
                                            0x0018: "VIDEO_MAP_TYPE",              
                                            0x0019: "SENSOR_MAP_TYPE",             
                                            0x001a: "CONTROL_TYPE",                
                                            0x001b: "SIGNAL_SELECTOR_TYPE",        
                                            0x001c: "MIXER_TYPE",                  
                                            0x001d: "MATRIX_TYPE",                 
                                            0x001e: "MATRIX_SIGNAL_TYPE",          
                                            0x001f: "SIGNAL_SPLITTER_TYPE",        
                                            0x0020: "SIGNAL_COMBINER_TYPE",        
                                            0x0021: "SIGNAL_DEMULTIPLEXER_TYPE",    
                                            0x0022: "SIGNAL_MULTIPLEXER_TYPE",        
                                            0x0023: "SIGNAL_TRANSCODER_TYPE",        
                                            0x0024: "CLOCK_DOMAIN_TYPE",            
                                            0x0025: "CONTROL_BLOCK_TYPE",            
                                            0xffff: "INVALID_TYPE"               
                                                          })  ,                 
                 XShortField("descriptor_id",0x3210)   ]
    
    
"""
typedef struct {
    unsigned char v_subtype;
    unsigned char format;
    unsigned char reserved0[2];
    unsigned char reserved1[4];
} avb_1722_1_aem_avtp_video_stream_format_t;
"""
    
class AVTP_AUDIO_FORMAT(Packet):
    name = "AVTP_AUDIO_FORMAT_Payload "  
    fields_desc=[ ByteEnumField("v_subtype", 0x02, {
                                            0x00: "SIX1883_IIDC_SUBTYPE" ,
                                            0x01: "MMA_SUBTYPE" ,
                                            0x02: "AVTP_AUDIO_SUBTYPE" ,
                                            0x03: "AVTP_VIDEO_SUBTYPE" ,
                                            0x04: "AVTP_CONTROL_SUBTYPE" ,
                                            0x6f: "VENDOR_SUBTYPE"
                                        
                                        }),
                 ByteEnumField("reserved_sample_rate", 5, {
                                            0: "SAMPLERATE_NOTSPECIFIED",
                                            1: "SAMPLERATE_8k",
                                            2: "SAMPLERATE_16k",
                                            3: "SAMPLERATE_32k",
                                            4: "SAMPLERATE_441k",
                                            5: "SAMPLERATE_48k",
                                            6: "SAMPLERATE_882k",
                                            7: "SAMPLERATE_96k",
                                            8: "SAMPLERATE_1764k",
                                            9: "SAMPLERATE_192k"
                                                    }),
                 ByteEnumField("format", 3, {
                                            0: "FORMAT_NOTSPECIFIED",
                                            1: "FORMAT_FLOAT",
                                            2: "FORMAT_I32",
                                            3: "FORMAT_PI24",
                                            4: "FORMAT_I16"
                                                    }),
                 XByteField("bit_depth", 0x18),
                 XByteField("channels_per_frame_lo", 0x00),
                 XByteField("channels_per_frame_hi_samples_per_frame_lo", 0x40),
                 XByteField("samples_per_frame_hi_reserved_lo", 0x00),
                 XByteField("reserved_hi", 0x00)
                 
                 ]

class AEM_GETSET_STREAM_FORMAT_RESP(Packet):
    name = "AEM_GETSET_STREAM_FORMAT_RESP_Payload "  
    fields_desc=[ ShortEnumField("descriptor_type",0x3210,{                                                          
                                            0x0000: "ENTITY_TYPE" ,                
                                            0x0001: "CONFIGURATION_TYPE",          
                                            0x0002: "AUDIO_UNIT_TYPE",             
                                            0x0003: "VIDEO_UNIT_TYPE",             
                                            0x0004: "SENDOR_UNIT_TYPE",            
                                            0x0005: "STREAM_INPUT_TYPE",           
                                            0x0006: "STREAM_OUTPUT_TYPE",          
                                            0x0007: "JACK_INPUT_TYPE",             
                                            0x0008: "JACK_OUTPUT_TYPE",            
                                            0x0009: "AVB_INTERFACE_TYPE",          
                                            0x000a: "CLOCK_SOURCE_TYPE",           
                                            0x000b: "MEMORY_OBJECT_TYPE",          
                                            0x000c: "LOCALE_TYPE",                 
                                            0x000d: "STRINGS_TYPE",                
                                            0x000e: "STREAM_PORT_INPUT_TYPE",      
                                            0x000f: "STREAM_PORT_OUTPUT_TYPE",     
                                            0x0010: "EXTERNAL_PORT_INPUT_TYPE",    
                                            0x0011: "EXTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0012: "INTERNAL_PORT_INPUT_TYPE",    
                                            0x0013: "INTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0014: "AUDIO_CLUSTER_TYPE",          
                                            0x0015: "VIDEO_CLUSTER_TYPE",          
                                            0x0016: "SENSOR_CLUSTER_TYPE",         
                                            0x0017: "AUDIO_MAP_TYPE",              
                                            0x0018: "VIDEO_MAP_TYPE",              
                                            0x0019: "SENSOR_MAP_TYPE",             
                                            0x001a: "CONTROL_TYPE",                
                                            0x001b: "SIGNAL_SELECTOR_TYPE",        
                                            0x001c: "MIXER_TYPE",                  
                                            0x001d: "MATRIX_TYPE",                 
                                            0x001e: "MATRIX_SIGNAL_TYPE",          
                                            0x001f: "SIGNAL_SPLITTER_TYPE",        
                                            0x0020: "SIGNAL_COMBINER_TYPE",        
                                            0x0021: "SIGNAL_DEMULTIPLEXER_TYPE",    
                                            0x0022: "SIGNAL_MULTIPLEXER_TYPE",        
                                            0x0023: "SIGNAL_TRANSCODER_TYPE",        
                                            0x0024: "CLOCK_DOMAIN_TYPE",            
                                            0x0025: "CONTROL_BLOCK_TYPE",            
                                            0xffff: "INVALID_TYPE"               
                                                          })  ,                 
                 XShortField("descriptor_id",0x3210)   ]
    
class AEM_SET_STREAM_FORMAT_CMD(Packet):
    name = "AEM_SET_STREAM_FORMAT_CMD_Payload "  
    fields_desc=[ ShortEnumField("descriptor_type",0x3210,{                                                          
                                            0x0000: "ENTITY_TYPE" ,                
                                            0x0001: "CONFIGURATION_TYPE",          
                                            0x0002: "AUDIO_UNIT_TYPE",             
                                            0x0003: "VIDEO_UNIT_TYPE",             
                                            0x0004: "SENDOR_UNIT_TYPE",            
                                            0x0005: "STREAM_INPUT_TYPE",           
                                            0x0006: "STREAM_OUTPUT_TYPE",          
                                            0x0007: "JACK_INPUT_TYPE",             
                                            0x0008: "JACK_OUTPUT_TYPE",            
                                            0x0009: "AVB_INTERFACE_TYPE",          
                                            0x000a: "CLOCK_SOURCE_TYPE",           
                                            0x000b: "MEMORY_OBJECT_TYPE",          
                                            0x000c: "LOCALE_TYPE",                 
                                            0x000d: "STRINGS_TYPE",                
                                            0x000e: "STREAM_PORT_INPUT_TYPE",      
                                            0x000f: "STREAM_PORT_OUTPUT_TYPE",     
                                            0x0010: "EXTERNAL_PORT_INPUT_TYPE",    
                                            0x0011: "EXTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0012: "INTERNAL_PORT_INPUT_TYPE",    
                                            0x0013: "INTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0014: "AUDIO_CLUSTER_TYPE",          
                                            0x0015: "VIDEO_CLUSTER_TYPE",          
                                            0x0016: "SENSOR_CLUSTER_TYPE",         
                                            0x0017: "AUDIO_MAP_TYPE",              
                                            0x0018: "VIDEO_MAP_TYPE",              
                                            0x0019: "SENSOR_MAP_TYPE",             
                                            0x001a: "CONTROL_TYPE",                
                                            0x001b: "SIGNAL_SELECTOR_TYPE",        
                                            0x001c: "MIXER_TYPE",                  
                                            0x001d: "MATRIX_TYPE",                 
                                            0x001e: "MATRIX_SIGNAL_TYPE",          
                                            0x001f: "SIGNAL_SPLITTER_TYPE",        
                                            0x0020: "SIGNAL_COMBINER_TYPE",        
                                            0x0021: "SIGNAL_DEMULTIPLEXER_TYPE",    
                                            0x0022: "SIGNAL_MULTIPLEXER_TYPE",        
                                            0x0023: "SIGNAL_TRANSCODER_TYPE",        
                                            0x0024: "CLOCK_DOMAIN_TYPE",            
                                            0x0025: "CONTROL_BLOCK_TYPE",            
                                            0xffff: "INVALID_TYPE"               
                                                          })  ,                 
                 XShortField("descriptor_id",0x3210)   ]
    
class AEM_GET_COUNTERS_CMD(Packet):
    name = "class AEM_GET_COUNTERS_CMD_Payload "  
    fields_desc=[ ShortEnumField("descriptor_type",0x3210,{                                                          
                                            0x0000: "ENTITY_TYPE" ,                
                                            0x0001: "CONFIGURATION_TYPE",          
                                            0x0002: "AUDIO_UNIT_TYPE",             
                                            0x0003: "VIDEO_UNIT_TYPE",             
                                            0x0004: "SENDOR_UNIT_TYPE",            
                                            0x0005: "STREAM_INPUT_TYPE",           
                                            0x0006: "STREAM_OUTPUT_TYPE",          
                                            0x0007: "JACK_INPUT_TYPE",             
                                            0x0008: "JACK_OUTPUT_TYPE",            
                                            0x0009: "AVB_INTERFACE_TYPE",          
                                            0x000a: "CLOCK_SOURCE_TYPE",           
                                            0x000b: "MEMORY_OBJECT_TYPE",          
                                            0x000c: "LOCALE_TYPE",                 
                                            0x000d: "STRINGS_TYPE",                
                                            0x000e: "STREAM_PORT_INPUT_TYPE",      
                                            0x000f: "STREAM_PORT_OUTPUT_TYPE",     
                                            0x0010: "EXTERNAL_PORT_INPUT_TYPE",    
                                            0x0011: "EXTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0012: "INTERNAL_PORT_INPUT_TYPE",    
                                            0x0013: "INTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0014: "AUDIO_CLUSTER_TYPE",          
                                            0x0015: "VIDEO_CLUSTER_TYPE",          
                                            0x0016: "SENSOR_CLUSTER_TYPE",         
                                            0x0017: "AUDIO_MAP_TYPE",              
                                            0x0018: "VIDEO_MAP_TYPE",              
                                            0x0019: "SENSOR_MAP_TYPE",             
                                            0x001a: "CONTROL_TYPE",                
                                            0x001b: "SIGNAL_SELECTOR_TYPE",        
                                            0x001c: "MIXER_TYPE",                  
                                            0x001d: "MATRIX_TYPE",                 
                                            0x001e: "MATRIX_SIGNAL_TYPE",          
                                            0x001f: "SIGNAL_SPLITTER_TYPE",        
                                            0x0020: "SIGNAL_COMBINER_TYPE",        
                                            0x0021: "SIGNAL_DEMULTIPLEXER_TYPE",    
                                            0x0022: "SIGNAL_MULTIPLEXER_TYPE",        
                                            0x0023: "SIGNAL_TRANSCODER_TYPE",        
                                            0x0024: "CLOCK_DOMAIN_TYPE",            
                                            0x0025: "CONTROL_BLOCK_TYPE",            
                                            0xffff: "INVALID_TYPE"               
                                                          })  ,                 
                 XShortField("descriptor_id",0x3210)   ]
    
class AEM_GET_COUNTERS_RESP(Packet):
    name = "AEM_GET_COUNTERS_RESP_Payload "  
    fields_desc=[ ShortEnumField("descriptor_type",0x3210,{                                                          
                                            0x0000: "ENTITY_TYPE" ,                
                                            0x0001: "CONFIGURATION_TYPE",          
                                            0x0002: "AUDIO_UNIT_TYPE",             
                                            0x0003: "VIDEO_UNIT_TYPE",             
                                            0x0004: "SENDOR_UNIT_TYPE",            
                                            0x0005: "STREAM_INPUT_TYPE",           
                                            0x0006: "STREAM_OUTPUT_TYPE",          
                                            0x0007: "JACK_INPUT_TYPE",             
                                            0x0008: "JACK_OUTPUT_TYPE",            
                                            0x0009: "AVB_INTERFACE_TYPE",          
                                            0x000a: "CLOCK_SOURCE_TYPE",           
                                            0x000b: "MEMORY_OBJECT_TYPE",          
                                            0x000c: "LOCALE_TYPE",                 
                                            0x000d: "STRINGS_TYPE",                
                                            0x000e: "STREAM_PORT_INPUT_TYPE",      
                                            0x000f: "STREAM_PORT_OUTPUT_TYPE",     
                                            0x0010: "EXTERNAL_PORT_INPUT_TYPE",    
                                            0x0011: "EXTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0012: "INTERNAL_PORT_INPUT_TYPE",    
                                            0x0013: "INTERNAL_PORT_OUTPUT_TYPE",   
                                            0x0014: "AUDIO_CLUSTER_TYPE",          
                                            0x0015: "VIDEO_CLUSTER_TYPE",          
                                            0x0016: "SENSOR_CLUSTER_TYPE",         
                                            0x0017: "AUDIO_MAP_TYPE",              
                                            0x0018: "VIDEO_MAP_TYPE",              
                                            0x0019: "SENSOR_MAP_TYPE",             
                                            0x001a: "CONTROL_TYPE",                
                                            0x001b: "SIGNAL_SELECTOR_TYPE",        
                                            0x001c: "MIXER_TYPE",                  
                                            0x001d: "MATRIX_TYPE",                 
                                            0x001e: "MATRIX_SIGNAL_TYPE",          
                                            0x001f: "SIGNAL_SPLITTER_TYPE",        
                                            0x0020: "SIGNAL_COMBINER_TYPE",        
                                            0x0021: "SIGNAL_DEMULTIPLEXER_TYPE",    
                                            0x0022: "SIGNAL_MULTIPLEXER_TYPE",        
                                            0x0023: "SIGNAL_TRANSCODER_TYPE",        
                                            0x0024: "CLOCK_DOMAIN_TYPE",            
                                            0x0025: "CONTROL_BLOCK_TYPE",            
                                            0xffff: "INVALID_TYPE"               
                                                          })  ,                 
                 XShortField("descriptor_id",0x3210),
                 XIntField("counters_valid",0x00000000), 
                 XIntField("counters_block0",0x00000000), 
                 XIntField("counters_block1",0x00000000), 
                 XIntField("counters_block2",0x00000000),   ]
    
    
                 
class AECP_AEM(Packet):
    name = "AECP_AEM_Packet "  
    fields_desc=[ ByteEnumField("cd_subtype",0xfb, {0xfb: "AECP"}) ,
                 ByteEnumField("sv_avb_version_msg_type",0x00,{                                                     
                                                        0: "AEM_COMMAND",
                                                        1: "AEM_RESPONSE"}) ,
                 ByteEnumField("status",0x00, {
                                            0: "SUCCESS",
                                            1: "NOT_IMPLEMENTED"
                                        }) ,
                 XByteField("data_length_lo",0x28),
                 XLongField("entity_id",0xfedcba9876543210) ,
                 XLongField("controller_id",0xfedcba9876543210) ,                 
                 XShortField("sequence_id",0x3210) ,
                 XByteField("uflag_command_type",0x80) ,
                 ByteEnumField("command_type",0,{
                                                        0: "ACQUIRE_ENTITY",
                                                        1: "LOCK_ENTITY" ,
                                                        2: "ENTITY_AVAILABLE" ,
                                                        3: "CONTROLLER_AVAILABLE" ,
                                                        4: "READ_DESCRIPTOR" ,
                                                        5: "WRITE_DESCRIPTOR" ,
                                                        6: "SET_CONFIGURATION" ,
                                                        7: "GET_CONFIGURATION" ,
                                                        8: "SET_STREAM_FORMAT" ,
                                                        9: "GET_STREAM_FORMAT",
                                                        10: "SET_VIDEO_FORMAT" ,
                                                        11: "GET_VIDEO_FORMAT" ,
                                                        12: "SET_SENSOR_FORMAT" ,
                                                        13: "GET_SENSOR_FORMAT" ,
                                                        14: "SET_STREAM_INFO" ,
                                                        15: "GET_STREAM_INFO" ,
                                                        16: "SET_NAME" ,
                                                        17: "GET_NAME" ,
                                                        18: "SET_ASSOCIATION_ID" ,
                                                        19: "GET_ASSOCIATION_ID" ,
                                                        20: "SET_SAMPLING_RATE" ,
                                                        21: "GET_SAMPLING_RATE" ,
                                                        22: "SET_CLOCK_SOURCE" ,
                                                        23: "GET_CLOCK_SOURCE" ,
                                                        24: "SET_CONTROL" ,
                                                        25: "GET_CONTROL" ,
                                                        26: "INCREMENT_CONTROL" ,
                                                        27: "DECREMENT_CONTROL" ,
                                                        28: "SET_SIGNAL_SELECTOR" ,
                                                        29: "GET_SIGNAL_SELECTOR" ,
                                                        30: "SET_MIXER" ,
                                                        31: "GET_MIXER" ,
                                                        32: "SET_MATRIX" ,
                                                        33: "GET_MATRIX" ,
                                                        34: "START_STREAMING" ,
                                                        35: "STOP_STREAMING" ,
                                                        36: "REGISTER_UNSOLICITED_NOTIFICATION" ,
                                                        37: "DEREGISTER_UNSOLICITED_NOTIFICATION" ,
                                                        38: "IDENTIFY_NOTIFICATION" ,
                                                        39: "GET_AVB_INFO" ,
                                                        40: "GET_AS_PATH" ,
                                                        41: "GET_COUNTERS" ,
                                                        42: "REBOOT" ,
                                                        43: "GET_AUDIO_MAP" ,
                                                        44: "ADD_AUDIO_MAPPINGS" ,
                                                        45: "REMOVE_AUDIO_MAPPINGS" ,
                                                        46: "GET_VIDEO_MAP" ,
                                                        47: "ADD_VIDEO_MAPPINGS" ,
                                                        48: "REMOVE_VIDEO_MAPPINGS" ,
                                                        49: "GET_SENSOR_MAP" ,
                                                        50: "ADD_SENSOR_MAPPINGS" ,
                                                        51: "REMOVE_SENSOR_MAPPINGS" ,
                                                        52: "START_OPERATION" ,
                                                        53: "ABORT_OPERATION" ,
                                                        54: "OPERATION_STATUS" ,
                                                        55: "AUTH_ADD_KEY" ,
                                                        56: "AUTH_DELETE_KEY" ,
                                                        57: "AUTH_GET_KEY_COUNT" ,
                                                        58: "AUTH_GET_KEY" ,
                                                        59: "AUTHENTICATE" ,
                                                        60: "DEAUTHENTICATE"
                                                    }) ]
    
    def mysummary(self):
        return self.sprintf("cd_subtype %cd_subtype%\n\
sv_avb_version_msg_type %sv_avb_version_msg_type%\n\
valid_time_data_length_hi %valid_time_data_length_hi%\n\
data_length_lo %data_length_lo%\n\
entity_id %entity_id%\n\entity_id %entity_id%\n\
entity_type %entity_type%")
    
    
    
    
    
class VENDOR_PAYLOAD_IPv4(Packet):
    name = "VENDOR_PAYLOAD_IPv4_Payload "  
    fields_desc=[ XByteField("version",0x04) ,
                 ShortField("udp_port",1234) ,
                 ByteField("ipv4_address0", 192),
                 ByteField("ipv4_address1", 168),
                 ByteField("ipv4_address2", 1),
                 ByteField("ipv4_address3", 1)
                 ]
    
class VENDOR_PAYLOAD_IPv6(Packet):
    name = "VENDOR_PAYLOAD_IPv6_Payload "  
    fields_desc=[ XByteField("version",0x06) ,
                 ShortField("udp_port",1234) ,
                 XShortField("ipv6_address0", 0xaaaa),
                 XShortField("ipv6_address1", 0xbbbb),
                 XShortField("ipv6_address2", 0xcccc),
                 XShortField("ipv6_address3", 0xdddd),
                 XShortField("ipv6_address4", 0xeeee),
                 XShortField("ipv6_address5", 0xffff),
                 XShortField("ipv6_address6", 0x1212),
                 XShortField("ipv6_address7", 0x3434),
                 ]
    
    
class VENDOR_PAYLOAD_ID64BIT(Packet):
    name = "VENDOR_PAYLOAD_ID64BIT_Payload "  
    fields_desc=[ 
                 XLongField("endstation_id", 0x0000000000000000)
                 ]
    
    
    
class AECP_VENDOR_CMD_RESP(Packet):
    name = "AECP_VENDOR_CMD_RESP_Payload "  
    fields_desc=[ ByteEnumField("command",0x01, {
                                                1: "V_CREATE",
                                                2: "V_MODIFY",
                                                3: "V_DESTROY",
                                                15: "V_QUIT"
                                                        }) ,
                 ByteEnumField("target",0x01,{        
                                                        1: "V_TALKER",
                                                        2: "V_LISTENER"
                                                     }),
                 ShortField("udp_payload_size",256)
                 ]


class AECP_VENDOR_RESP(Packet):
    name = "AECP_VENDOR_RESP_Payload "  
    fields_desc=[ 
                 XLongField("stream_id", 0x0000000000000000),
                 XLongField("endstation_id", 0x0000000000000000),
                 XShortField("endstation_local_id", 0x0000),
                 DestMACField("stream_dest_mac")                 
                 ]
                 
class AECP_VENDOR(Packet):
    name = "AECP_VENDOR_Packet "  
    fields_desc=[ ByteEnumField("cd_subtype",0xfb, {0xfb: "AECP"}) ,
                 ByteEnumField("sv_avb_version_msg_type",6,{        
                                                        6: "VENDOR_UNIQUE_COMMAND",
                                                        7: "VENDOR_UNIQUE_RESPONSE"
                                                     }) ,
                 ByteEnumField("status",0x00, {
                                            0: "SUCCESS",
                                            1: "NOT_IMPLEMENTED",
                                            2: "FAILURE"
                                        }) ,
                 XByteField("data_length_lo",0x28),
                 XLongField("entity_id",0xfedcba9876543210) ,
                 XLongField("controller_id",0xfedcba9876543210) ,                 
                 XShortField("sequence_id",0x3210) ,
                 XShortField("protocol_id_lo",0x70b3) ,
                 XIntField("protocol_id_hi",0xd5eddead) ]
    
    def mysummary(self):
        return self.sprintf("cd_subtype %cd_subtype%\n\
sv_avb_version_msg_type %sv_avb_version_msg_type%\n\
valid_time_data_length_hi %valid_time_data_length_hi%\n\
data_length_lo %data_length_lo%\n\
entity_id %entity_id%\n\entity_id %entity_id%\n\
entity_type %entity_type%")















class ACMP(Packet):
    name = "ACMP_Packet "  
    
    fields_desc=[ ByteEnumField("cd_subtype",0xfc, {0xfc: "ACMP"}) ,      
                 ByteEnumField("sv_avb_version_message_type",0x00,{                                                     
                                                        0: "CONNECT_TX_COMMAND",
                                                        1: "CONNECT_TX_RESPONSE",
                                                        2: "DISCONNECT_TX_COMMAND",
                                                        3: "DISCONNECT_TX_RESPONSE",
                                                        4: "GET_TX_STATE_COMMAND",
                                                        5: "GET_TX_STATE_RESPONSE",
                                                        6: "CONNECT_RX_COMMAND   ",
                                                        7: "CONNECT_RX_RESPONSE",
                                                        8: "DISCONNECT_RX_COMMAND",
                                                        9: "DISCONNECT_RX_RESPONSE",
                                                        10: "GET_RX_STATE_COMMAND",
                                                        11: "GET_RX_STATE_RESPONSE",
                                                        12: "GET_TX_CONNECTION_COMMAND",
                                                        13: "GET_TX_CONNECTION_RESPONSE" 
                                                     }) ,
                 ByteEnumField("status",0x00, {
                                                        0: "SUCCESS",
                                                        1: "LISTENER_UNKNOWN_ID",
                                                        2: "TALKER_UNKNOWN_ID",
                                                        3: "TALKER_DEST_MAC_FAIL",
                                                        4: "TALKER_NO_STREAM_INDEX",
                                                        5: "TALKER_NO_BANDWIDTH",
                                                        6: "TALKER_EXCLUSIVE",
                                                        7: "LISTENER_TALKER_TIMEOUT",
                                                        8: "LISTENER_EXCLUSIVE",
                                                        9: "STATE_UNAVAILABLE",
                                                        10: "NOT_CONNECTED",
                                                        11: "NO_SUCH_CONNECTION",
                                                        12: "COULD_NOT_SEND_MESSAGE",
                                                        13: "TALKER_MISBEHAVING",
                                                        14: "LISTENER_MISBEHAVING",
                                                        15: "SRP_FACE",
                                                        16: "CONTROLLER_NOT_AUTHORIZED",
                                                        17: "INCOMPATIBLE_REQUEST",
                                                        31: "NOT_SUPPORTED",
                                               }) ,
                 XByteField("data_length_lo",0x2c),
                 XLongField("stream_id",0xfedcba9876543210) ,
                 XLongField("controller_id",0xfedcba9876543210) ,
                 XLongField("talker_id",0xfedcba9876543210) ,
                 XShortField("talker_unique_id",0x3210) ,
                 XLongField("listener_id",0xfedcba9876543210) ,
                 XShortField("listener_unique_id",0x3210) ,
                 DestMACField("stream_dest_mac") ,
                 XShortField("connection_count",0x3210) ,
                 XShortField("sequence_id",0x3210) ,
                 XShortField("flags",0x3210) ,
                 XIntField("default_format",0x76543210) ]
    
    def mysummary(self):
        return self.sprintf("cd_subtype %cd_subtype%\n\
sv_avb_version_message_type %sv_avb_version_message_type%\n\
status %status%\n\
data_length_lo %data_length_lo%\n\
stream_id %stream_id%\n\
controller_id %controller_id%\n\
talker_id %talker_id%\n\
listener_id %listener_id%\n\
talker_unique_id %talker_unique_id%\n\
listener_unique_id %listener_unique_id%\n\
stream_dest_mac %stream_dest_mac%\n\
connection_count %connection_count%\n\
sequence_id %sequence_id%\n\
flags %flags%\n\
default_format %default_format%")    
    

bind_layers( AEM_GETSET_STREAM_FORMAT_RESP, AVTP_AUDIO_FORMAT )
bind_layers( AEM_SET_STREAM_FORMAT_CMD, AVTP_AUDIO_FORMAT )

bind_layers( AECP_AEM, AEM_READ_DESCRIPTOR_CMD )
bind_layers( AECP_AEM, AEM_READ_DESCRIPTOR_RESP )
bind_layers( AECP_AEM, AEM_ACQUIRE_ENTITY_CMD )
bind_layers( AECP_AEM, AEM_GET_AVB_INFO_CMD )
bind_layers( AECP_AEM, AEM_GET_AVB_INFO_RESP )
bind_layers( AECP_AEM, AEM_LOCK_ENTITY_CMD )
bind_layers( AECP_AEM, AEM_START_STOP_STREAMING_CMD )
bind_layers( AECP_AEM, AEM_GET_STREAM_FORAT_CMD )
bind_layers( AECP_AEM, AEM_GETSET_STREAM_FORMAT_RESP )
bind_layers( AECP_AEM, AEM_SET_STREAM_FORMAT_CMD )
bind_layers( AECP_AEM, AEM_GET_COUNTERS_CMD )
bind_layers( AECP_AEM, AEM_GET_COUNTERS_RESP )

bind_layers( Ether, AECP_AEM )



bind_layers( VENDOR_PAYLOAD_IPv4, AECP_VENDOR_RESP)
bind_layers( VENDOR_PAYLOAD_IPv6, AECP_VENDOR_RESP)
bind_layers( VENDOR_PAYLOAD_ID64BIT, AECP_VENDOR_RESP)

bind_layers( AECP_VENDOR_CMD_RESP, VENDOR_PAYLOAD_IPv4)
bind_layers( AECP_VENDOR_CMD_RESP, VENDOR_PAYLOAD_IPv6)
bind_layers( AECP_VENDOR_CMD_RESP, VENDOR_PAYLOAD_ID64BIT)

bind_layers( AECP_VENDOR, AECP_VENDOR_CMD_RESP)

bind_layers( Ether, AECP_VENDOR)





























bind_layers( Ether, ADP )

bind_layers( Ether, ACMP )