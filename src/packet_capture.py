'''
Created on Jul 22, 2014

@author: christoph
'''
import sys, time, socket
from struct import *

from PyQt5 import QtCore, QtGui, QtWidgets



class Packet_Capture(object):
    def __init__(self, parent, netif):
        #QtCore.QObject.__init__()       
        self.qt = parent.qt
        
        self.net_if = str(netif)          
        self.cols = 64        
        self.index = 0
        self.workerThread = WorkThread(self.net_if)
        
        self.qt.tableWidget.setColumnCount(self.cols)
        for i in range(0,self.cols):
            self.qt.tableWidget.setColumnWidth(i,30)
            
        #self.qt.connect(self.qt.checkBox, QtCore.SIGNAL("stateChanged(int)"), self.checkBoxState)
        #self.qt.connect(self.qt, QtCore.SIGNAL("close()"), self.workerThread.terminate)   
    #-------------------------------------------------------------------------------------------------------------------------
           
    
        
    def checkBoxState(self, state):
        if self.qt.checkBox.isChecked() == True:
            self.qt.connect(self.workerThread, QtCore.SIGNAL("update(QString)"), self.capture)
            self.workerThread.start()
            print("start thread "+str(state))
        else:
            self.workerThread.stopRunning()
            #self.workerThread = None
            print("stop thread "+str(state))
    #-------------------------------------------------------------------------------------------------------------------------
      
    
    def capture(self, packet_qstring):
        self.index += 1
        packet_string = str(packet_qstring)
        packet_array = packet_string.split(",")
        
        self.qt.tableWidget.setRowCount(self.index)
        self.qt.tableWidget.insertRow(self.index)    
        for i, field in enumerate(packet_array[:len(packet_array)-1]):
            item = QtGui.QTableWidgetItem()
            item.setText(field)
            self.qt.tableWidget.setItem(self.index, i, item)
    #-------------------------------------------------------------------------------------------------------------------------

#=======================================================================================================================      
   
   
   
   
"""BPF Filtering

# load proto(ethertype field at byte offset 12)
bpf_stmt(BPF_LD | BPF_H | BPF_ABS, 12),
# CHECK IF ethertype== 0x7788, if equal skip 1 statement
bpf_jump(BPF_JMP | BPF_JEQ | BPF_K, 0x7788, 1, 0),
# CHECK IF ethertype== 0x7799, if not equal skip 1 statement
bpf_jump(BPF_JMP | BPF_JEQ | BPF_K, 0x7799, 0, 1),
bpf_stmt(BPF_RET | BPF_K, 0x0fffffff), # pass
bpf_stmt(BPF_RET | BPF_K, 0), # reject 


from binascii import hexlify
from ctypes import create_string_buffer, addressof
from socket import socket, AF_PACKET, SOCK_RAW, SOL_SOCKET
from struct import pack, unpack


# A subset of Berkeley Packet Filter constants and macros, as defined in
# linux/filter.h.

# Instruction classes
BPF_LD = 0x00
BPF_JMP = 0x05
BPF_RET = 0x06

# ld/ldx fields
BPF_H = 0x08
BPF_B = 0x10
BPF_ABS = 0x20

# alu/jmp fields
BPF_JEQ = 0x10
BPF_K = 0x00

def bpf_jump(code, k, jt, jf):
    return pack('HBBI', code, jt, jf, k)

def bpf_stmt(code, k):
    return bpf_jump(code, k, 0, 0)


# Ordering of the filters is backwards of what would be intuitive for 
# performance reasons: the check that is most likely to fail is first.
filters_list = [
    # Must have dst port 67. Load (BPF_LD) a half word value (BPF_H) in 
    # ethernet frame at absolute byte offset 36 (BPF_ABS). If value is equal to
    # 67 then do not jump, else jump 5 statements.
    bpf_stmt(BPF_LD | BPF_H | BPF_ABS, 36),
    bpf_jump(BPF_JMP | BPF_JEQ | BPF_K, 67, 0, 5),

    # Must be UDP (check protocol field at byte offset 23)
    bpf_stmt(BPF_LD | BPF_B | BPF_ABS, 23), 
    bpf_jump(BPF_JMP | BPF_JEQ | BPF_K, 0x11, 0, 3),

    # Must be IPv4 (check ethertype field at byte offset 12)
    bpf_stmt(BPF_LD | BPF_H | BPF_ABS, 12), 
    bpf_jump(BPF_JMP | BPF_JEQ | BPF_K, 0x0800, 0, 1),

    bpf_stmt(BPF_RET | BPF_K, 0x0fffffff), # pass
    bpf_stmt(BPF_RET | BPF_K, 0), # reject
]

# Create filters struct and fprog struct to be used by SO_ATTACH_FILTER, as
# defined in linux/filter.h.
filters = ''.join(filters_list)
b = create_string_buffer(filters)
mem_addr_of_filters = addressof(b)
fprog = pack('HL', len(filters_list), mem_addr_of_filters)

# As defined in asm/socket.h
SO_ATTACH_FILTER = 26

# Create listening socket with filters
s = socket(AF_PACKET, SOCK_RAW, 0x0800)
s.setsockopt(SOL_SOCKET, SO_ATTACH_FILTER, fprog)
s.bind(('eth0', 0x0800))

while True:
    data, addr = s.recvfrom(65565)
    print 'got data from', addr, ':', hexlify(data)



"""
class WorkThread(QtCore.QThread):
    def __init__(self, net_if):
        QtCore.QThread.__init__(self)
        self.net_if = net_if
        self.isRunning = False
        print("worker init " +self.net_if)
#         self.s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
        self.rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
        #self.s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    #-------------------------------------------------------------------------------------------------------------------------
      

    
    def __del__(self):
        self.rawSocket.close() 
        self.wait()
    #-------------------------------------------------------------------------------------------------------------------------
      
    
    def stopRunning(self):
        self.isRunning = False
#         self.wait()          
    #-------------------------------------------------------------------------------------------------------------------------
    
    def close_event(self):        
        self.rawSocket.close()
        self.terminate()          
    #-------------------------------------------------------------------------------------------------------------------------
      
    
    def run(self):
        self.isRunning = True
        while(self.isRunning == True):
            fields=""            
            
            packet = self.rawSocket.recvfrom(65565)
            #packet string from tuple
            packet = packet[0]

            for i, j in enumerate(packet):
                fields += str(hex(j))+","
#                 print(str(hex(j))+" ")

#             packet = self.s.recvfrom(65565)
#             #packet string from tuple
#             packet = packet[0]
#             
#             #take first 20 characters for the ip header
#             ip_header = packet[0:20]
#             
#             #now unpack them :)
#             iph = unpack('!BBHHHBBH4s4s' , ip_header)
#             
#             version_ihl = iph[0]
#             version = version_ihl >> 4
#             ihl = version_ihl & 0xF
#             
#             iph_length = ihl * 4
#             
#             ttl = iph[5]
#             protocol = iph[6]
#             s_addr = socket.inet_ntoa(iph[8]);
#             d_addr = socket.inet_ntoa(iph[9]);
#             
#             #fields +='Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)
#             fields += str(version) + "," + str(ihl) + "," + str(ttl) + "," + str(protocol) + "," + str(s_addr) + "," + str(d_addr) + ","
#             
#             tcp_header = packet[iph_length:iph_length+20]
#             
#             #now unpack them :)
#             tcph = unpack('!HHLLBBHHH' , tcp_header)
#             
#             source_port = tcph[0]
#             dest_port = tcph[1]
#             sequence = tcph[2]
#             acknowledgement = tcph[3]
#             doff_reserved = tcph[4]
#             tcph_length = doff_reserved >> 4
#             
#             #fields += ' Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)
#             fields += str(source_port) + "," + str(dest_port) + "," + str(sequence) + "," + str(acknowledgement) + "," + str(tcph_length)
#             
#             h_size = iph_length + tcph_length * 4
#             data_size = len(packet) - h_size
#             
#             #get data from the packet
#             #data = packet[h_size:]
#             
#             #print( 'Data : ' + str(data))
    
            self.emit( QtCore.SIGNAL('update(QString)'), fields )
            fields =""
        print("closing...")    
        #self.terminate()
        print("closed")
    #-------------------------------------------------------------------------------------------------------------------------
      
      
      
 #=======================================================================================================================
 
 
 
