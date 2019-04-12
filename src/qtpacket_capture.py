# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/qtpacket_capture.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(798, 598)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 60, 781, 531))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(20, 20, 91, 21))
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.checkBox.setText(_translate("Dialog", "Capturing"))

