'''
Created on April 16, 2019

@author: christoph
'''
import mmap
import os
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import posix_ipc

import ipc_utils as utils
from avdeccEntity import AVDECCEntity, serializeList2Str, deserializeStr2List
from avdecccmdlineWrapper import AVDECC_Controller
  
headerBGColor = QtGui.QColor(125,125,125)  
connectedBGColor = QtGui.QColor(0,255,0) 
connectingBGColor = QtGui.QColor(128,229,255) 
defaultBGColor = QtGui.QColor(255,255,255) 
cornerBGColor = QtGui.QColor(120,0,0) 

class JackAVBfactory(QtWidgets.QMainWindow):
    '''Main Class'''
    def __init__(self) :                
        QtWidgets.QMainWindow.__init__(self) 
        self.qt = uic.loadUi('qt/mainWindow.ui',self)
        #self.qt = Ui_MainWindow()
        #self.qt.setupUi(self)

        self.params = utils.read_params()

        # Create the shared memory and the semaphore.
        self.memory = posix_ipc.SharedMemory(self.params["SHARED_MEMORY_NAME"], posix_ipc.O_CREX, size=self.params["SHM_SIZE"])
        self.semaphore = posix_ipc.Semaphore(self.params["SEMAPHORE_NAME"], posix_ipc.O_CREX)

        # Create the message queue.
        self.mq = posix_ipc.MessageQueue(self.params["MESSAGE_QUEUE_NAME"], posix_ipc.O_CREX)

        # MMap the shared memory
        self.mapfile = mmap.mmap(self.memory.fd, self.memory.size)

        self.semaphore.release()
        
        self.listeners = []
        self.talkers = []
        
        
        self.avdecccmdline_wrapper_thread()
        
             
        self.cols = 1
        self.rows = 1 
        self.endpointType = "l"
                
        self.qt.tableWidget.setColumnCount(self.cols)
        self.qt.tableWidget.setRowCount(self.rows)
        
        self.qt.tableWidget.horizontalHeader().setVisible(False)
        self.qt.tableWidget.verticalHeader().setVisible(False)
        
        self.qt.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("")) 
        self.qt.tableWidget.item(0, 0).setBackground(cornerBGColor)
                        
        self.qt.tableWidget.cellClicked.connect(self.cellClickedSlot)
        self.qt.radioButton.toggled.connect(self.qt.setEndpointTypeTalker)
        self.qt.radioButton_2.toggled.connect(self.qt.setEndpointTypeListener)
        self.qt.pushButton.clicked.connect(self.createJACKClient) 

        self.show()      

        self.mq.send("list")    
        time.sleep(5)   
        msg = ""
        while(not "ack" in msg):
            msg, _ = self.mq.receive()
            msg = msg.decode()
    
        self.updateAVBEntityList()
         
    #-------------------------------------------------------------------------------------------------------------------------
    
    def setEndpointTypeListener(self, state):
        if state:
            self.endpointType = "l"
    #-------------------------------------------------------------------------------------------------------------------------
        
    def setEndpointTypeTalker(self, state):
        if state:
            self.endpointType = "t"
    #-------------------------------------------------------------------------------------------------------------------------
            
    def addEntityToTable(self, entity, m, n, endpointType):
#        self.qt.textEdit.clear()
        self.qt.textEdit.append( "###########################################################" )
        self.qt.textEdit.append( "Creating JACK AVB %s: %s"%( entity.endpointType, entity.jackclient_name) )
        self.qt.textEdit.append( "MAC Address: %s"%( entity.MACAddr.decode("utf8") ) )
        self.qt.textEdit.append( "Stream Id: %s"%( entity.streamId.decode("utf8") ) )
        self.qt.textEdit.append( "Stream Destination MAC: %s"%( entity.destMAC.decode("utf8") ) )
        self.qt.textEdit.append( "Channel Count Talker: %d"%( entity.channelCountTalker ) )
        self.qt.textEdit.append( "Channel Count Listener: %d"%( entity.channelCountListener ) )
                
        if endpointType == "l":  
            self.rows += 1   
            self.qt.tableWidget.insertRow(m)   
            self.qt.tableWidget.setRowCount(m+1)
        elif endpointType == "t":
            self.cols += 1
            self.qt.tableWidget.insertColumn(n) 
            self.qt.tableWidget.setColumnCount(n+1) 
                
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(headerBGColor)        
        item.setText(entity.jackclient_name + entity.name) 
        self.qt.tableWidget.setItem(m, n, item)
                          
        if endpointType == "l":  
            for i in range(1,self.cols):        
                self.qt.tableWidget.setItem(m, i, QtWidgets.QTableWidgetItem('O'))
                self.qt.tableWidget.item(m, i).setBackground(defaultBGColor)
        elif endpointType == "t":
            for i in range(1,self.rows):        
                self.qt.tableWidget.setItem(i, n, QtWidgets.QTableWidgetItem('O'))
                self.qt.tableWidget.item(i, n).setBackground(defaultBGColor)
    #-------------------------------------------------------------------------------------------------------------------------
    
    def createJACKClient(self):
        entity =  AVDECCEntity()     
        entity.jackclient_name = str(self.qt.lineEdit_3.text())
        entity.name = ""
        entity.entityId = bytearray( ("".join( str(self.qt.lineEdit.text()).split(":") ) ).encode("utf8") )
        entity.firmwareVersion = ""
        entity.MACAddr = bytearray( ("".join( str(self.qt.lineEdit_5.text()).split(":") ) ).encode("utf8") )
        entity.endpointType = self.endpointType
        if "l" in entity.endpointType:
            entity.channelCountListener = int(self.qt.spinBox.value())
        else :
            entity.channelCountTalker = int(self.qt.spinBox.value())
        entity.sampleRate_k = 48
        entity.destMAC = bytearray( ("".join( str(self.qt.lineEdit_2.text()).split(":") ) ).encode("utf8") )
        entity.streamId = bytearray( ("".join( str(self.qt.lineEdit.text()).split(":") ) ).encode("utf8") )
        
        if entity.endpointType == "l":    
            entity.idx = self.rows     
            self.listeners.append(entity)        
            self.addEntityToTable(entity, entity.idx, 0, "l")
        elif entity.endpointType == "t":    
            entity.idx = self.cols
            self.talkers.append(entity)
            self.addEntityToTable(entity, 0, entity.idx, "t")
    #-------------------------------------------------------------------------------------------------------------------------
        
    def updateAVBEntityList(self):
        self.semaphore.acquire()
        serStr = utils.read_from_memory(self.mapfile)
        self.semaphore.release()

        serList = deserializeStr2List(serStr)

        for device in serList:    
            entity = AVDECCEntity()  
            if entity.decodeString(device) > 0: # return values -1, 1
                print(entity.endpointType)
                if "t" in entity.endpointType:   
                    entity.idx = self.cols               
                    self.talkers.append(entity)
                    self.addEntityToTable(entity, 0, self.cols, "t")
                if "l" in entity.endpointType:   
                    entity.idx = self.rows            
                    self.listeners.append(entity)
                    self.addEntityToTable(entity, self.rows, 0, "l")
            else:
                break
    #-------------------------------------------------------------------------------------------------------------------------
     
    def cellClickedSlot(self, i, j):
        print(i,j)    
        if j == 0 or i == 0:
            self.showEntityDetails(i, j)
        else:
            self.connectStream(i, j)
    #-------------------------------------------------------------------------------------------------------------------------
    
       
    def findEntity(self, i, j):
            
        foundEntity = 0
        for listener in self.listeners:
            #print(listener.name, listener.jackclient_name, str(self.qt.tableWidget.item(i,j).text()))
            if listener.name == str(self.qt.tableWidget.item(i,j).text()):
                self.qt.lineEdit_4.setText(listener.name)
                foundEntity = 1
            elif listener.jackclient_name == str(self.qt.tableWidget.item(i,j).text()):
                self.qt.lineEdit_4.setText(listener.jackclient_name)
                foundEntity = 2
                
            if foundEntity > 0:
                return listener
                
        for talker in self.talkers:
            #print(talker.name, talker.jackclient_name, str(self.qt.tableWidget.item(i,j).text()))
            if talker.name == str(self.qt.tableWidget.item(i,j).text()):
                self.qt.lineEdit_4.setText(talker.name)
                foundEntity = 1
            elif talker.jackclient_name == str(self.qt.tableWidget.item(i,j).text()):
                self.qt.lineEdit_4.setText(talker.jackclient_name)
                foundEntity = 2
                
            if foundEntity > 0:
                return talker
        return None  
    #-------------------------------------------------------------------------------------------------------------------------
    
    
    def connectStream(self, i, j):    
        if str(self.qt.tableWidget.item(i,j).text()) == 'O': 
            for n in range(1,self.cols):
                self.qt.tableWidget.item(i,n).setText('')
                self.qt.tableWidget.item(i,n).setBackground(defaultBGColor)
            self.qt.tableWidget.item(i,j).setText('...')
            self.qt.tableWidget.item(i,j).setBackground(connectingBGColor)
            self.qt.textEdit.append( "l -..-..-..-> t" )
            self.qt.textEdit.append( "JACK AVB Listener Client: %s waiting for connection to AVB Talker %s"%( self.qt.tableWidget.item(i,0).text(), self.qt.tableWidget.item(0,j).text()) )


            entity = self.findEntity(i, j)


        elif str(self.qt.tableWidget.item(i,j).text()) == '...': 
            self.qt.tableWidget.item(i,j).setText('X')
            self.qt.tableWidget.item(i,j).setBackground(connectedBGColor)
            self.qt.textEdit.append( "l ----------> t" )
            self.qt.textEdit.append( "Activating JACK AVB Listener Client: %s and connecting to AVB Talker %s"%( self.qt.tableWidget.item(i,0).text(), self.qt.tableWidget.item(0,j).text()) )


            entity = self.findEntity(i, j)


        elif str(self.qt.tableWidget.item(i,j).text()) == 'X':  
        
            for n in range(1,self.cols):
                self.qt.tableWidget.item(i,n).setText('O')
                self.qt.tableWidget.item(i,n).setBackground(defaultBGColor)
            self.qt.tableWidget.item(i,j).setText('O')
            self.qt.tableWidget.item(i,j).setBackground(defaultBGColor)
            self.qt.textEdit.append( "l xxxxxxxxxxxx t" )
            self.qt.textEdit.append( "Disconnecting JACK AVB Listener Client: %s from AVB Talker %s and dectivating JACK Client"%( self.qt.tableWidget.item(i,0).text(), self.qt.tableWidget.item(0,j).text()) )


            entity = self.findEntity(i, j)


    #-------------------------------------------------------------------------------------------------------------------------
    
    
    def showEntityDetails(self, i, j):
        entity = self.findEntity(i, j)
        #entity.entityId = bytearray( ("".join( str(self.qt.lineEdit.text()).split(":") ) ).encode("utf8") )
        #entity.firmwareVersion = ""
        if entity is None:
            return -1
        
        if "l" in entity.endpointType:
            self.qt.radioButton.toggle()
            self.qt.spinBox.setValue(entity.channelCountListener)
        if "t" in entity.endpointType:
            self.qt.radioButton_2.toggle()
            self.qt.spinBox.setValue(entity.channelCountTalker)
                    
        printMac = ""   
        i = 0
        while( i < len(entity.MACAddr.decode("utf8"))):
            if i != 0 and i < len(entity.MACAddr.decode("utf8"))-1:
                printMac += ":"
            printMac += entity.MACAddr.decode("utf8")[i:i+2]
            i += 2            
        self.qt.lineEdit_5.setText( printMac )
        #entity.endpointType
        #entity.sampleRate_k
        printDst = ""   
        i = 0
        while( i < len(entity.MACAddr.decode("utf8"))):
            if i != 0 and i < len(entity.MACAddr.decode("utf8"))-1:
                printDst += ":"
            printDst += entity.destMAC.decode("utf8")[i:i+2]
            i += 2            
        self.qt.lineEdit_2.setText( printDst )
        
        printSid = ""   
        i = 0
        while( i < len(entity.MACAddr.decode("utf8"))):
            if i != 0 and i < len(entity.MACAddr.decode("utf8"))-1:
                printSid += ":"
            printSid += entity.streamId.decode("utf8")[i:i+2]
            i += 2            
        self.qt.lineEdit.setText( printSid )


    #-------------------------------------------------------------------------------------------------------------------------
       
    def avdecccmdline_wrapper_thread(self):
        self.avdecc_thread = QtCore.QThread()
        self.avdeccctl = AVDECC_Controller("enp1s0")
        self.avdeccctl.moveToThread(self.avdecc_thread)
        self.avdecc_thread.started.connect(self.avdeccctl.run_avdecccmdline_thread)
        self.avdecc_thread.start() 
    #-------------------------------------------------------------------------------------------------------------------------
              
    def closeEvent(self, event):

        quit_msg = "Are you sure you want to exit the program?"
        reply = QtWidgets.QMessageBox.question(self, 'Message', quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
    
        if reply == QtWidgets.QMessageBox.Yes:  
            #self.mq.send("quit")
            #time.sleep(2)
            self.avdecc_thread.terminate()
        
            self.mapfile.close()
            posix_ipc.unlink_shared_memory(self.params["SHARED_MEMORY_NAME"])

            self.mq.close()
            posix_ipc.unlink_message_queue(self.params["MESSAGE_QUEUE_NAME"])

            self.semaphore.release()
            self.semaphore.unlink()
            event.accept()          
        else:
            event.ignore()
    #-------------------------------------------------------------------------------------------------------------------------
#=======================================================================================================================
      

if __name__ == '__main__':

    qApp = QtWidgets.QApplication(sys.argv)
    pyqtavdecc = JackAVBfactory()
    sys.exit(qApp.exec_())   
    pass
    
    
