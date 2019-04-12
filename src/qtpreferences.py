# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/qtpreferences.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(668, 288)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(310, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(160, 10, 113, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 111, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 371, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 70, 641, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Preferences"))
        self.lineEdit.setText(_translate("Dialog", "wlan0"))
        self.label.setText(_translate("Dialog", "Network Interface"))
        self.label_2.setText(_translate("Dialog", "AVDECC CMDLine Path"))
        self.lineEdit_2.setText(_translate("Dialog", "/home/christoph/source_code/python/pyAVDECC/PyQtAVDECC/avdecc-lib/controller/app/cmdline/"))

