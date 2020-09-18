# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'componentInstructionsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(570, 464)
        self.continueButton = QtWidgets.QPushButton(Dialog)
        self.continueButton.setGeometry(QtCore.QRect(380, 420, 75, 23))
        self.continueButton.setObjectName("continueButton")
        self.logoLabel = QtWidgets.QLabel(Dialog)
        self.logoLabel.setGeometry(QtCore.QRect(420, 60, 131, 51))
        self.logoLabel.setText("")
        self.logoLabel.setPixmap(QtGui.QPixmap("../images/GWA_logo.png"))
        self.logoLabel.setScaledContents(True)
        self.logoLabel.setObjectName("logoLabel")
        self.topLabel = QtWidgets.QLabel(Dialog)
        self.topLabel.setGeometry(QtCore.QRect(20, 70, 401, 41))
        self.topLabel.setWordWrap(True)
        self.topLabel.setObjectName("topLabel")
        self.instructionsFooterLabel = QtWidgets.QLabel(Dialog)
        self.instructionsFooterLabel.setGeometry(QtCore.QRect(30, 330, 501, 21))
        self.instructionsFooterLabel.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.instructionsFooterLabel.setWordWrap(True)
        self.instructionsFooterLabel.setObjectName("instructionsFooterLabel")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(20, 140, 531, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setGeometry(QtCore.QRect(470, 420, 75, 23))
        self.cancelButton.setObjectName("cancelButton")
        self.instructionsHeaderLabel = QtWidgets.QLabel(Dialog)
        self.instructionsHeaderLabel.setGeometry(QtCore.QRect(20, 150, 101, 41))
        self.instructionsHeaderLabel.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.instructionsHeaderLabel.setWordWrap(True)
        self.instructionsHeaderLabel.setObjectName("instructionsHeaderLabel")
        self.bottomLabel = QtWidgets.QLabel(Dialog)
        self.bottomLabel.setGeometry(QtCore.QRect(20, 380, 511, 31))
        self.bottomLabel.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.bottomLabel.setWordWrap(True)
        self.bottomLabel.setObjectName("bottomLabel")
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(20, 360, 531, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.instructionsMainLabel = QtWidgets.QLabel(Dialog)
        self.instructionsMainLabel.setGeometry(QtCore.QRect(30, 160, 511, 131))
        self.instructionsMainLabel.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.instructionsMainLabel.setWordWrap(True)
        self.instructionsMainLabel.setObjectName("instructionsMainLabel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "GWA Toolbox Installation"))
        self.continueButton.setText(_translate("Dialog", "Continue"))
        self.topLabel.setText(_translate("Dialog", "BEAM is a software for analysing optical and thermal data derived with satellites operated by Europen Space Agency (ESA) and other organisation."))
        self.instructionsFooterLabel.setText(_translate("Dialog", "Afterwards click \"Continue\"."))
        self.cancelButton.setText(_translate("Dialog", "Cancel"))
        self.instructionsHeaderLabel.setText(_translate("Dialog", "Instructions:"))
        self.bottomLabel.setText(_translate("Dialog", "If you would like to abandon the installation altogether, click \"Cancel\". The GWA Toolbox components that were already installed will remain on your computer."))
        self.instructionsMainLabel.setText(_translate("Dialog", "You need to activate BEAM plugins. To do that start BEAM, select \"Plugins\" from main menu and ..."))

