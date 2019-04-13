'''
Created on Jul 21, 2014

@author: christoph
'''
import sys, time, subprocess
from PyQt5 import QtCore, QtGui, QtWidgets

from qtavdecc_listener_factory import Ui_MainWindow

  
class PyQtAVDECC(QtWidgets.QMainWindow):
    '''Main Class'''
    def __init__(self) :                
        QtWidgets.QMainWindow.__init__(self) 
        self.qt = Ui_MainWindow()
        self.qt.setupUi(self)
        
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
    
    
