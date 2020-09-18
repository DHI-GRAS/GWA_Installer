# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'installComponentDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(570, 464)
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(20, 320, 531, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setGeometry(QtCore.QRect(470, 420, 75, 23))
        self.cancelButton.setObjectName("cancelButton")
        self.topLabel = QtWidgets.QLabel(Dialog)
        self.topLabel.setGeometry(QtCore.QRect(20, 70, 401, 41))
        self.topLabel.setWordWrap(True)
        self.topLabel.setObjectName("topLabel")
        self.installButton = QtWidgets.QPushButton(Dialog)
        self.installButton.setGeometry(QtCore.QRect(290, 420, 75, 23))
        self.installButton.setObjectName("installButton")
        self.bottomLabel2 = QtWidgets.QLabel(Dialog)
        self.bottomLabel2.setGeometry(QtCore.QRect(20, 380, 511, 31))
        self.bottomLabel2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.bottomLabel2.setWordWrap(True)
        self.bottomLabel2.setObjectName("bottomLabel2")
        self.bottomLabel1 = QtWidgets.QLabel(Dialog)
        self.bottomLabel1.setGeometry(QtCore.QRect(20, 340, 511, 31))
        self.bottomLabel1.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.bottomLabel1.setWordWrap(True)
        self.bottomLabel1.setObjectName("bottomLabel1")
        self.skipButton = QtWidgets.QPushButton(Dialog)
        self.skipButton.setGeometry(QtCore.QRect(380, 420, 75, 23))
        self.skipButton.setObjectName("skipButton")
        self.instructionMainLabel = QtWidgets.QLabel(Dialog)
        self.instructionMainLabel.setGeometry(QtCore.QRect(30, 180, 511, 61))
        self.instructionMainLabel.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.instructionMainLabel.setWordWrap(True)
        self.instructionMainLabel.setObjectName("instructionMainLabel")
        self.componentLogoLabel = QtWidgets.QLabel(Dialog)
        self.componentLogoLabel.setGeometry(QtCore.QRect(420, 90, 131, 51))
        self.componentLogoLabel.setText("")
        self.componentLogoLabel.setPixmap(QtGui.QPixmap("../images/beamLogo.png"))
        self.componentLogoLabel.setScaledContents(False)
        self.componentLogoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.componentLogoLabel.setObjectName("componentLogoLabel")
        self.instructionsHeaderLabel = QtWidgets.QLabel(Dialog)
        self.instructionsHeaderLabel.setGeometry(QtCore.QRect(20, 150, 101, 41))
        self.instructionsHeaderLabel.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.instructionsHeaderLabel.setWordWrap(True)
        self.instructionsHeaderLabel.setObjectName("instructionsHeaderLabel")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(20, 140, 531, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.logoLabel = QtWidgets.QLabel(Dialog)
        self.logoLabel.setGeometry(QtCore.QRect(420, 30, 131, 51))
        self.logoLabel.setText("")
        self.logoLabel.setPixmap(QtGui.QPixmap("../images/GWA_logo.png"))
        self.logoLabel.setScaledContents(True)
        self.logoLabel.setObjectName("logoLabel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "GWA Toolbox Installation"))
        self.cancelButton.setText(_translate("Dialog", "Cancel"))
        self.topLabel.setText(_translate("Dialog", "BEAM is a software for analysing optical and thermal data derived with satellites operated by Europen Space Agency (ESA) and other organisation."))
        self.installButton.setText(_translate("Dialog", "Install"))
        self.bottomLabel2.setText(_translate("Dialog", "If you would like to abandon the installation altogether, click \"Cancel\". The GWA Toolbox components that were already installed will remain on your computer."))
        self.bottomLabel1.setText(_translate("Dialog", "If you do not want to install this GWA Toolbox component click \"Skip\" to go the installation of the next component. However, note that by doing so you will not get the full GWA Toolbox functionality."))
        self.skipButton.setText(_translate("Dialog", "Skip"))
        self.instructionMainLabel.setText(_translate("Dialog", "After clicking on the \"Install\" button the BEAM installer will start. In the installer you will be asked to accept the BEAM licence conditions followed by a couple of installation questions. In all the questions you can keep the defauly answers by clicking \"Next >\" untill the installation starts."))
        self.instructionsHeaderLabel.setText(_translate("Dialog", "Instructions:"))

