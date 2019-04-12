'''
Created on Jul 21, 2014

@author: christoph
'''
import subprocess, sys, time, threading, queue
from Cython import *
# from

# cdef extern from "/home/christoph/source_code/avb/avdecc-lib/controller/lib/include/controller.h":
# #             cdef cppclass net_interface
# #                 pass
#             pass

class ADP(object):
    def __init__(self, preferences):
        self.preferences = preferences
 
        """cmd_line.cpp line 100 -> init controller"""
        """cmd_line.cpp line 900 -> list command"""
        
        
        
        self.load_lib()
        
        print("ADP initialized!")
 
    #-------------------------------------------------------------------------------------------------------------
    
    def load_lib(self):
        
#         try: # %self.preferences.qt.lineEdit_2.text()
#             cdef extern from "/home/christoph/source_code/avb/avdecc-lib/controller/lib/include/controller.h":
#                 cdef cppclass net_interface
#                 pass
#             cdef extern from "/home/christoph/source_code/avb/avdecc-lib/controller/lib/include/controller.h" namespace "avdecc_lib":
#                 cdef cppclass end_station
#                     pass
#                 cdef cppclass configuration_descriptor
#                     pass
#                 cdef cppclass controller:         
#                     AVDECC_CONTROLLER_LIB32_API virtual void STDCALL destroy() = 0;
#                     AVDECC_CONTROLLER_LIB32_API virtual const char * STDCALL get_version() const = 0;
#                     AVDECC_CONTROLLER_LIB32_API virtual size_t STDCALL get_end_station_count() = 0;
#                     AVDECC_CONTROLLER_LIB32_API virtual end_station * STDCALL get_end_station_by_index(size_t end_station_index) = 0;
#                     AVDECC_CONTROLLER_LIB32_API virtual bool STDCALL is_end_station_found_by_entity_id(uint64_t entity_entity_id, uint32_t &end_station_index) = 0;
#                     AVDECC_CONTROLLER_LIB32_API virtual configuration_descriptor * STDCALL get_current_config_desc(size_t end_station_index, bool report_error=true) = 0;
#                     AVDECC_CONTROLLER_LIB32_API virtual configuration_descriptor * STDCALL get_config_desc_by_entity_id(uint64_t end_station_entity_id, uint16_t entity_index, uint16_t config_index) = 0;
#                     AVDECC_CONTROLLER_LIB32_API virtual void STDCALL set_logging_level(int32_t new_log_level) = 0;
#                     AVDECC_CONTROLLER_LIB32_API virtual uint32_t STDCALL missed_notification_count() = 0;
#                     AVDECC_CONTROLLER_LIB32_API virtual uint32_t STDCALL missed_log_count() = 0;
#                     AVDECC_CONTROLLER_LIB32_API virtual int STDCALL send_controller_avail_cmd(void *notification_id, uint32_t end_station_index) = 0;
#                     extern "C" AVDECC_CONTROLLER_LIB32_API controller * STDCALL create_controller(net_interface *netif, void (*notification_callback) (void *notification_user_obj, int32_t notification_type, uint64_t entity_id, uint16_t cmd_type, uint16_t desc_type, uint16_t desc_index, uint32_t cmd_status, void *notification_id), void (*log_callback) (void *log_user_obj, int32_t log_level, const char *log_msg, int32_t time_stamp_ms), int32_t initial_log_level);
#                     pass
#                 pass
# }
                
                
                
                
            #self.avdecc_lib = windll.kernel32(self.preferences.qt.lineEdit_2.text()+"libcontroller.so")
            print("Controller Library loaded!")
#         except ImportError:
#             print("Could not load Controller Library")
    #-------------------------------------------------------------------------------------------------------------
            
    def init_controller(self):
#                 void (*notification_callback) (void *, int32_t, uint64_t, uint16_t, uint16_t, uint16_t, uint32_t, void *),
#                 void (*log_callback) (void *, int32_t, const char *, int32_t),

        self.current_end_station = 0
    
        #Start non-zero so as not to be confused with commands without notification
        self.notification_id = 1
    
    
        """https://gist.github.com/nzjrs/990493"""    
#     me = os.path.abspath(os.path.dirname(__file__))
# lib = cdll.LoadLibrary(os.path.join(me, "..", "libtest.so"))
#  
# func = lib.test_get_data_nulls
# func.restype = POINTER(c_char)
# func.argtypes = [POINTER(c_int)]
#  
# l = c_int()
# data = func(byref(l))
#  
# print data,l,data.contents
#  
# lib.test_data_print(data,l)
#  
# func_out = lib.test_get_data_nulls_out
# func_out.argtypes = [POINTER(POINTER(c_char)), POINTER(c_int)]
# func.restype = None
#  
# l2 = c_int()
# data2 = POINTER(c_char)()
# func_out(byref(data2), byref(l2))
#  
# print data2,l2,data2.contents
#  
# lib.test_data_print(data2,l2)
#  
# print "equal ", data[0]==data2[0], data[1]==data2[1], data[2]==data2[2], data[3]==data2[3], data[4]==data2[4]        
        
        

#         self.netif = self.avdecc_lib.create_net_interface()
#                         
#         self.controller_obj = self.avdecc_lib.create_controller(self.netif, None, None, 0)#notification_callback, log_callback, 0)
# netif = avdecc_lib::create_net_interface();
# controller_obj = avdecc_lib::create_controller(netif, notification_callback, log_callback, log_level);
# sys = avdecc_lib::create_system(avdecc_lib::system::LAYER2_MULTITHREADED_CALLBACK, netif, controller_obj);
# 
# atomic_cout << "AVDECC Controller version: " << controller_obj->get_version() << std::endl;
# print_interfaces_and_select(interface);
# sys->process_start();
        
#         print(getattr(cdll.msvcrt, "avdecc_lib::create_controller") )
#         self.sys = self.avdecc_lib.create_system(0,self.netif,self.controller_obj)
#         print("sys: " + str(self.sys))
#         
#         self.sys.process_start()
    #-------------------------------------------------------------------------------------------------------------
           
        
    def __del__(self):
        self.sys.process_close();
        self.sys.destroy();
        self.controller_obj.destroy();
        self.netif.destroy();
        self.ofstream_ref.close();
    #-------------------------------------------------------------------------------------------------------------
            
            
    def avdecc_list(self):
    
#         print("\n End Station  |  Name  |  Entity ID  |  Firmware Version  |  MAC\n")
#         
#         for(unsigned int i = 0; i < self.controller_obj->get_end_station_count(); i++)
#             avdecc_lib::end_station *end_station = self.controller_obj->get_end_station_by_index(i);
#     
#             if (end_station)
#                 uint64_t end_station_entity_id = end_station->entity_id();
#                 avdecc_lib::entity_descriptor *ent_desc = NULL;
#                 
#                 if (end_station->entity_desc_count())
#                     uint16_t current_entity = end_station->get_current_entity_index();
#                     ent_desc = end_station->get_entity_desc_by_index(current_entity);
#                     
#                 const char *end_station_name = "";
#                 const char *fw_ver = "";
#                 
#                 if (ent_desc)
#                     end_station_name = (const char *)ent_desc->entity_name();
#                     fw_ver = (const char *)ent_desc->firmware_version();
#                 uint64_t end_station_mac = end_station->mac();
#                 print(end_station->get_connection_status(), 
#                       i, 
#                       ent_desc ? end_station_name : "UNKNOWN", 
#                       end_station_entity_id, 
#                       ent_desc ? fw_ver : "UNKNOWN", 
#                       end_station_mac.rdbuf())
            
        pass
    
#=================================================================================================================