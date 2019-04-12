'''
Created on Jul 21, 2014

@author: christoph
'''
import sys, time, subprocess
from PyQt5 import QtCore, QtGui, QtWidgets

from qtavdecc_listener_factory import Ui_MainWindow
from qtpacket_capture import Ui_Dialog
from packet_capture import Packet_Capture

  
class PyQtAVDECC(QtWidgets.QMainWindow):
    '''Main Class'''
    def __init__(self) :                
        QtWidgets.QMainWindow.__init__(self) 
        self.qt = Ui_MainWindow()
        self.qt.setupUi(self)
        
        self.packet_capture = Packet_Capture(self, "wlp3s0")

                
                
        #self.connect(self.qt.pushButton, QtCore.SIGNAL("clicked()"), self.packet_capture.qt.show)
#         self.connect(self.ui.actionExit, QtCore.SIGNAL("close()"), self.closeEvent)
#         self.connect(self.ui.actionExit, QtCore.SIGNAL("close()"), self.packet_capture.closeEvent)


        self.show()
    #-------------------------------------------------------------------------------------------------------------------------
       
       
    def closeEvent(self, event):

        quit_msg = "Are you sure you want to exit the program?"
        reply = QtGui.QMessageBox.question(self, 'Message', 
                         quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
    
        if reply == QtGui.QMessageBox.Yes:  
            event.accept()          
        else:
            event.ignore()
    #-------------------------------------------------------------------------------------------------------------------------
#=======================================================================================================================
      

if __name__ == '__main__':

    qApp = QtWidgets.QApplication(sys.argv)
    pyqtavdecc = PyQtAVDECC()
    sys.exit(qApp.exec_())   
    pass
    
    
