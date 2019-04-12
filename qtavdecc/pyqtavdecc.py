'''
Created on Jul 21, 2014

@author: christoph
'''
import sys, time, subprocess
from PyQt4 import QtGui, QtCore, Qt

from qtavdecc import Ui_QtAVDECC
from qtpacket_capture import Ui_Dialog
from packet_capture import Packet_Capture
from qtpreferences import Ui_Dialog as Ui_Preferences
from preferences import Preferences
from _adp import ADP

  
class PyQtAVDECC(QtGui.QMainWindow):
    '''Main Class'''
    def __init__(self) :                
        QtGui.QMainWindow.__init__(self) 
        self.qt = Ui_QtAVDECC()
        self.qt.setupUi(self)
        
        self.preferences =  Preferences()
        self.packet_capture = Packet_Capture(self, self.preferences)

                
                
        self.connect(self.qt.pushButton, QtCore.SIGNAL("clicked()"), self.packet_capture.qt.show)
        self.connect(self.qt.actionPreferences, QtCore.SIGNAL("triggered()"), self.preferences.qt.show)         
        self.connect(self.preferences.qt.buttonBox, QtCore.SIGNAL("accepted()"), self.preferences.qt.accept)
        self.connect(self.preferences.qt.buttonBox, QtCore.SIGNAL("rejected()"), self.preferences.qt.reject)
#         self.connect(self.ui.actionExit, QtCore.SIGNAL("close()"), self.closeEvent)
#         self.connect(self.ui.actionExit, QtCore.SIGNAL("close()"), self.packet_capture.closeEvent)


        self.adp_instance = ADP(self.preferences)
        self.adp_instance.init_controller()
        print(self.adp_instance)
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

    qApp = QtGui.QApplication(sys.argv)
    pyqtavdecc = PyQtAVDECC()
    sys.exit(qApp.exec_())   
    pass