'''
Created on Jul 22, 2014

@author: christoph
'''
from PyQt4 import QtCore, QtGui
from qtpreferences import Ui_Dialog

class Preferences(object):
    def __init__(self):        
        self.qt = Ui_Dialog()
        self.qt.setupUi(self.qt)
        self.qt.lineEdit.setText("eth0")
        self.qt.lineEdit_2.setText("/home/christoph/source_code/avb/avdecc-lib/controller/lib/")
        pass
        
    def get_prefs(self):        
        return self