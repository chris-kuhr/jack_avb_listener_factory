'''
Created on Jul 21, 2014

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

#from mainWindow import Ui_MainWindow
  
headerBGColor = QtGui.QColor(125,125,125)  
connectedBGColor = QtGui.QColor(0,255,0) 
connectingBGColor = QtGui.QColor(128,229,255) 
defaultBGColor = QtGui.QColor(255,255,255) 


headerFontColor = QtGui.QColor(255,255,255)  
defaultFontColor = QtGui.QColor(0,0,0)   

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

        # MMap the shared memory
        self.mapfile = mmap.mmap(self.memory.fd, self.memory.size)

        self.semaphore.release()
        
        '''
        self.avdecccmdline_wrapper_thread()
        '''
             
        self.cols = 17   
        self.rows = 1 
        self.index = 0
        self.endpointType = "Listener"
        
        self.namesT = ["","T1","T2","T3","T4","T5","T6","T7","T8","T9","T10","T11","T12","T13","T14","T15","T16"]
        
        self.namesL = [""]
        
        self.qt.tableWidget.setColumnCount(self.cols)
        self.qt.tableWidget.setRowCount(self.rows)
        
        self.qt.tableWidget.verticalHeader().setVisible(False)
        self.qt.tableWidget.horizontalHeader().setVisible(False)
        
        for i in range(1,self.cols):                    # set col width
            self.qt.tableWidget.setColumnWidth(i,50)                       
                       
        for i in range(1,self.cols):                    # set col label
            item = QtWidgets.QTableWidgetItem()         
            item.setText(self.namesT[i])
            item.setBackground(headerBGColor)
            #item.itemClicked.connect(self.showEntityDetails(int))
            self.qt.tableWidget.setItem(0, i, item)                       
                       
        for j in range(1,self.rows):                    # set row label
            item = QtWidgets.QTableWidgetItem()
            item.setText(self.namesL[j])
            item.setBackground(headerBGColor)
            self.qt.tableWidget.setItem(j, 0, item)
                       
        for j in range(1,self.rows):                    # populate table
#            self.qt.tableWidget.insertRow(j)    
            for i in range(1,self.cols):
                item = QtWidgets.QTableWidgetItem()
                item.setText('O')
                item.setBackground(defaultBGColor)
                self.qt.tableWidget.setItem(j, i, item)
                        
        self.qt.tableWidget.cellClicked.connect(self.cellClickedSlot)
        self.qt.radioButton.toggled.connect(self.qt.setEndpointTypeTalker)
        self.qt.radioButton_2.toggled.connect(self.qt.setEndpointTypeListener)
        self.qt.pushButton.clicked.connect(self.createJACKClient)        
        self.show()        
    #-------------------------------------------------------------------------------------------------------------------------
    
    def setEndpointTypeListener(self, state):
        if state:
            self.endpointType = "Listener"
            print(self.endpointType)
    #-------------------------------------------------------------------------------------------------------------------------
    
    
    def setEndpointTypeTalker(self, state):
        if state:
            self.endpointType = "Talker"
            print(self.endpointType)
    #-------------------------------------------------------------------------------------------------------------------------
    
    def createJACKClient(self):
#        self.qt.textEdit.clear()
        self.qt.textEdit.append( "Creating JACK AVB %s: %s"%( self.endpointType, str(self.qt.lineEdit_3.text()) ) )
        self.qt.textEdit.append( "AVB Device Name: %s"%( str(self.qt.lineEdit_4.text()) ) )
        self.qt.textEdit.append( "MAC Address: %s"%( str(self.qt.lineEdit_5.text()) ) )
        self.qt.textEdit.append( "Stream Id: %s"%( str(self.qt.lineEdit.text()) ) )
        self.qt.textEdit.append( "Stream Destination MAC: %s"%( str(self.qt.lineEdit_2.text()) ) )
        self.qt.textEdit.append( "Channel Count: %d"%( int(self.qt.spinBox.value()) ) )
        self.qt.tableWidget.insertRow(self.rows)   
        
        item = QtWidgets.QTableWidgetItem()
        item.setText(str(self.qt.lineEdit_3.text()))
        item.setBackground(headerBGColor)
        self.qt.tableWidget.setItem(self.rows, 0, item)
          
        for i in range(1,self.cols):
            item = QtWidgets.QTableWidgetItem()
            item.setText('O')
            item.setBackground(defaultBGColor)
            self.qt.tableWidget.setItem(self.rows, i, item)
            
        self.rows += 1
        self.qt.tableWidget.setRowCount(self.rows) 
    #-------------------------------------------------------------------------------------------------------------------------
    
    
    def cellClickedSlot(self, i, j):
        print(i,j)    
        if j == 0 or i == 0:
            self.showEntityDetails(i, j)
        else:
            self.connectStream(i, j)
    #-------------------------------------------------------------------------------------------------------------------------
       
    
    def connectStream(self, i, j):
        if str(self.qt.tableWidget.item(i,j).text()) == 'O': 
            for n in range(1,self.cols):
                self.qt.tableWidget.item(i,n).setText('')
                self.qt.tableWidget.item(i,n).setBackground(defaultBGColor)
            self.qt.tableWidget.item(i,j).setText('...')
            self.qt.tableWidget.item(i,j).setBackground(connectingBGColor)
            self.qt.textEdit.append( "JACK AVB Listener Client: %s waiting for connection to AVB Talker %s"%( self.qt.tableWidget.item(i,0).text(), self.qt.tableWidget.item(0,j).text()) )
        elif str(self.qt.tableWidget.item(i,j).text()) == '...': 
            self.qt.tableWidget.item(i,j).setText('X')
            self.qt.tableWidget.item(i,j).setBackground(connectedBGColor)
            self.qt.textEdit.append( "Activating JACK AVB Listener Client: %s and connecting to AVB Talker %s"%( self.qt.tableWidget.item(i,0).text(), self.qt.tableWidget.item(0,j).text()) )
        elif str(self.qt.tableWidget.item(i,j).text()) == 'X':  
        
            for n in range(1,self.cols):
                self.qt.tableWidget.item(i,n).setText('O')
                self.qt.tableWidget.item(i,n).setBackground(defaultBGColor)
            self.qt.tableWidget.item(i,j).setText('O')
            self.qt.tableWidget.item(i,j).setBackground(defaultBGColor)
            self.qt.textEdit.append( "Disconnecting JACK AVB Listener Client: %s from AVB Talker %s and dectivating JACK Client"%( self.qt.tableWidget.item(i,0).text(), self.qt.tableWidget.item(0,j).text()) )
    #-------------------------------------------------------------------------------------------------------------------------
       
    def showEntityDetails(self, i, j):
        self.qt.lineEdit_4.setText(str(self.qt.tableWidget.item(i,j).text()))
        if j != 0:
            pass
        elif i != 0:
            pass
    #-------------------------------------------------------------------------------------------------------------------------
       
    def avdecccmdline_wrapper_thread(self):
        self.avdecc_thread = QtCore.QThread()
        self.avdeccctl = AVDECC_Controller()
        self.avdeccctl.moveToThread(self.avdecc_thread)
        self.avdecc_thread.started.connect(self.avdeccctl.run_avdecccmdline_thread)
        self.avdecc_thread.start() 
    #-------------------------------------------------------------------------------------------------------------------------
       
    def updateEntityList(self):
        self.semaphore.acquire()
        serStr = utils.read_from_memory(self.mapfile)
        self.semaphore.release()

        serList = deserializeStr2List(serStr)

        entity_list2 = []
        for device in serList:    
            dummy = AVDECCEntity()  
            if dummy.decodeString(device) > 0: # return values -1, 1
                entity_list2.append(dummy)
                print(dummy.encodeString())
            else:
                break
    #-------------------------------------------------------------------------------------------------------------------------
       
    def closeEvent(self, event):

        quit_msg = "Are you sure you want to exit the program?"
        reply = QtWidgets.QMessageBox.question(self, 'Message', quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
    
        if reply == QtWidgets.QMessageBox.Yes:          
            # I could call memory.unlink() here but in order to demonstrate
            # unlinking at the module level I'll do it that way.
            posix_ipc.unlink_shared_memory(self.params["SHARED_MEMORY_NAME"])

            self.semaphore.release()

            # I could also unlink the semaphore by calling
            # posix_ipc.unlink_semaphore() but I'll do it this way instead.
            self.semaphore.unlink()
            self.mapfile.close()
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
    
    
