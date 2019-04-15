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
             
        self.cols = 16   
        self.rows = 16     
        self.index = 0
        
        self.names = ["one","two","three","four","five","six","seven","eight","nine","ten", "eleven","twelve", "thirteen","fourteen", "fivteen","sixteen"]
        
        self.qt.tableWidget.setColumnCount(self.cols)
        self.qt.tableWidget.setRowCount(self.rows)
        
        for i in range(1,self.cols):                    # set col width
            self.qt.tableWidget.setColumnWidth(i,50)                       
                       
        for i in range(1,self.cols):                    # set col label
            item = QtWidgets.QTableWidgetItem()         
            item.setText(self.names[i])
            #item.itemClicked.connect(self.showEntityDetails(int))
            self.qt.tableWidget.setItem(0, i, item)                       
                       
        for j in range(1,self.rows):                    # set row label
            item = QtWidgets.QTableWidgetItem()
            item.setText(self.names[j])
            self.qt.tableWidget.setItem(j, 0, item)
                       
        for j in range(1,self.rows):                    # populate table
#            self.qt.tableWidget.insertRow(j)    
            for i in range(1,self.cols):
                item = QtWidgets.QTableWidgetItem()
                item.setText('O')
                self.qt.tableWidget.setItem(j, i, item)
                        
        self.qt.tableWidget.cellClicked.connect(self.showEntityDetails)
        
        
        self.show()        
    #-------------------------------------------------------------------------------------------------------------------------
    
    def showEntityDetails(self, i, j):
        print(i,j)    
        if j != 0:
            self.qt.lineEdit_4.setText(self.names[j])
        elif i != 0:
            self.qt.lineEdit_4.setText(self.names[i])
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
    
    
