"""
***************************************************************************
   installerGUI.py
-------------------------------------
    Copyright (C) 2016 globWetland Africa (www.globwetland-africa.org)

***************************************************************************
* The GlobWetland Africa toolbox has been developed as part of the Glob-  *
* Wetland Africa project funded by the European Space Agency (ESA) in     *
* partnership with the Africa Team of the Ramsar Convention on Wetlands.  *
*                                                                         *
* The Toolbox is a free software i.e. you can redistribute it and/or      *
* modify it under the terms of the GNU General Public License as publis-  *
* hed by the Free Software Foundation, either version 3 of the License,   *
* or (at your option) any later version.                                  *
*                                                                         *
* The Toolbox is distributed in the hope that it will be useful, but      *
* WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTA-   *
* BILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public *
* License for more details.                                               *
*                                                                         *
* You should have received a copy of the GNU General Public License along *
* with this program.  If not, see <http://www.gnu.org/licenses/>.         *
***************************************************************************
"""
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from ui import welcomeDialog, installComponentDialog
from ui import postInstallComponentDialog, componentInstructionsDialog

# MACROS
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

# CONSTANTS
CANCEL = QtWidgets.QDialog.Rejected
NEXT = QtWidgets.QDialog.Accepted
SKIP = QtWidgets.QDialog.Accepted + 1

WINDOW_TITLE = "GWA Toolbox Installation - Install {name}"


DESCRIPTIONS = {
    'OSGeo4W': (
        "QGIS is the main GUI used by GWA Toolbox while Orfeo Toolbox and GRASS GIS "
        "provide many of the commonly used data processing functions. They are installed "
        "together through the OSGeo4W installer."),
    'SNAP': (
        "Snap Toolbox is a software for analyzing data derived with satellites operated "
        "by European Space Agency (ESA) and other organisations."),
    'R': (
        "R is a statistical scripting language used by GWA Toolbox for various "
        "data processing tasks.")
}

INSTALL_INSTRUCTIONS = {
    'OSGeo4W': (
        "After clicking on the \"Install\" button the OSGeo4W installer will start. "
        "The process should be automatic but if any question dialogs pop-up just click OK."),
    "SNAP": (
        "After clicking on the \"Install\" button the Snap Toolbox installer will start. "
        "SNAP is licensed under GNU General Public Lincense version 3 (GPLv3) and by starting the "
        "installation you accept the lincese condition. The installation is fully automatic and "
        "may take some time to complete."),
    'R': (
        "After clicking on the \"Install\" button the R installer will start. "
        "In the installer you will be asked to accept the R license conditions "
        "followed by a couple of installation questions. In all the questions "
        "you can keep the default answers by clicking \"Next >\" until the "
        "installation starts."),
}

LOGOS = {
    'main': 'images/GWA_logo.png',
    'main_ico': "images/GWA.ico",
    'OSGeo4W': "images/osgeo4wLogo.png",
    'SNAP': "images/snapLogo.png",
    'R': "images/rLogo.png",
}


UNINSTALL_LABEL = (
    "For a smooth installation process, some of the old components of GWA Toolbox "
    "have to be uninstalled if they are present on your computer.")

UNINSTALL_INSTRUCTIONS = (
    "Please follow the uninstallation instructions present in the 'GWA Toolbox installation' "
    "document located in the GWA Toolbox installation directory.")

POSTINSTALL_INSTRUCTIONS = (
    "The GWA Toolbox installer will now perform additional post-installation "
    "tasks for {name}. If you changed the {name} installation directory during "
    "the previous step (or skipped the step), make sure that you check the "
    "path to the directory below and update it if necessary.")


# #################################################################################
# Parent classes
# Used to avoid overwriting the files produced by QtDesigner and pyuic4
# Mostly assign actions to buttons and set up the dialog

class installerBaseWindow():
    def __init__(self, MainWindow=None):
        if MainWindow:
            self.MainWindow = MainWindow
        else:
            self.MainWindow = QtWidgets.QDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(LOGOS['main_ico'])),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MainWindow.setWindowIcon(icon)

    def exec_(self):
        return(self.MainWindow.exec_())

    def cancel(self):
        self.MainWindow.done(CANCEL)

    def next(self):
        self.MainWindow.done(NEXT)

    def skip(self):
        self.MainWindow.done(SKIP)


class installerWelcomeWindow(installerBaseWindow, welcomeDialog.Ui_Dialog):

    def __init__(self):
        installerBaseWindow.__init__(self)
        self.setupUi(self.MainWindow)
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(LOGOS['main'])))

        self.beginButton.clicked.connect(self.next)
        self.cancelButton.clicked.connect(self.cancel)
        self.beginButton.setFocus()


class installWindow(installerBaseWindow, installComponentDialog.Ui_Dialog):

    def __init__(self):
        installerBaseWindow.__init__(self)
        self.setupUi(self.MainWindow)
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(LOGOS['main'])))

        self.installButton.clicked.connect(self.next)
        self.skipButton.clicked.connect(self.skip)
        self.cancelButton.clicked.connect(self.cancel)
        self.installButton.setFocus()


class postInstallWindow(installerBaseWindow, postInstallComponentDialog.Ui_Dialog):

    def __init__(self):
        installerBaseWindow.__init__(self)
        self.setupUi(self.MainWindow)
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(LOGOS['main'])))

        self.continueButton.clicked.connect(self.next)
        self.skipButton.clicked.connect(self.skip)
        self.cancelButton.clicked.connect(self.cancel)
        self.dirSelectionButton.clicked.connect(self.dirSelection)
        self.continueButton.setFocus()

    def dirSelection(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(directory=self.dirPathText.toPlainText())
        if not path.isNull():
            self.dirPathText.setPlainText(_translate("MainWindow", path, None))


class instructionsWindow(installerBaseWindow, componentInstructionsDialog.Ui_Dialog):

    # This window can have a reimplemented QDialog used as the main window to allow
    # for multithreaded operations while the window is displayed
    def __init__(self, MainWindow=None):

        installerBaseWindow.__init__(self, MainWindow)
        self.setupUi(self.MainWindow)
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(LOGOS['main'])))

        self.continueButton.clicked.connect(self.next)
        self.cancelButton.clicked.connect(self.cancel)
        self.continueButton.setFocus()


# ##############################################################################
# Child classes
# Individualise the parent classes mostly by changing the text


class GenericInstallWindow(installWindow):

    def __init__(self, name):
        self.name = name
        installWindow.__init__(self)
        self.componentLogoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(LOGOS[self.name])))

    def retranslateUi(self, MainWindow):
        super(GenericInstallWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate(
            "MainWindow", DESCRIPTIONS[self.name], None))
        self.instructionMainLabel.setText(_translate(
            "MainWindow", INSTALL_INSTRUCTIONS[self.name], None))
        self.MainWindow.setWindowTitle(_translate(
            "MainWindow", WINDOW_TITLE.format(name=self.name), None))


class DirPathPostInstallWindow(postInstallWindow):

    def __init__(self, name, default_path):
        self.name = name
        self.default_path = default_path
        postInstallWindow.__init__(self)
        self.componentLogoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(LOGOS[name])))

    def retranslateUi(self, MainWindow):
        super(DirPathPostInstallWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate(
            "MainWindow", DESCRIPTIONS[self.name], None))
        self.instructionsMainLabel.setText(_translate(
            "MainWindow", POSTINSTALL_INSTRUCTIONS.format(name=self.name), None))
        self.dirPathText.setPlainText(_translate(
            "MainWindow", self.default_path, None))
        self.MainWindow.setWindowTitle(_translate(
            "MainWindow", WINDOW_TITLE.format(name=self.name), None))


# Instructions for activating GWA Toolbox plugins
class uninstallInstructionsWindow(instructionsWindow):
    def __init__(self):
        instructionsWindow.__init__(self)

    def retranslateUi(self, MainWindow):
        super(uninstallInstructionsWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate("MainWindow", UNINSTALL_INSTRUCTIONS, None))
        self.instructionsMainLabel.setText(_translate("MainWindow", UNINSTALL_INSTRUCTIONS, None))
        self.MainWindow.setWindowTitle(_translate(
            "MainWindow", "GWA Toolbox Installation - Uninstall old version", None))


class finishWindow(instructionsWindow):
    def __init__(self):
        instructionsWindow.__init__(self)

    def retranslateUi(self, MainWindow):
        super(finishWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate(
            "MainWindow", "The GWA Toolbox has now been installed on your computer. Thank you.", None))
        self.instructionsMainLabel.setText(_translate(
            "MainWindow", "You can now start QGIS to begin working with the GWA Toolbox.", None))
        self.continueButton.setVisible(False)
        self.instructionsHeaderLabel.setVisible(False)
        self.bottomLabel.setVisible(False)
        self.instructionsFooterLabel.setText(_translate(
            "MainWindow", "Click \"Finish\" to finish the installation process", None))
        self.MainWindow.setWindowTitle(_translate(
            "MainWindow", "GWA Toolbox Installation - Finished", None))
        self.cancelButton.setText(_translate("MainWindow", "Finish", None))


class cmdWaitWindow(instructionsWindow, QtCore.QObject):

    def __init__(self, utilities, cmd, **kwargs):
        QtCore.QObject.__init__(self)

        self.utilities = utilities
        self.cmd = cmd
        self.execute_kwargs = kwargs

        # Use a thread and modified QDialog to display the waiting dialog and
        # run the cmd at the same time
        self.workerThread = QtCore.QThread(self)
        self.MainWindow = myQDialog(self.workerThread)
        instructionsWindow.__init__(self, self.MainWindow)

        self.utilities.moveToThread(self.workerThread)
        self.utilities.finished.connect(self.workerThread.quit)
        self.workerThread.finished.connect(self.slotFinished)
        self.workerThread.started.connect(self.startAction)

    def retranslateUi(self, MainWindow):
        super(cmdWaitWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate(
            "MainWindow", "Running an external install command. Please wait...", None))
        self.instructionsMainLabel.setVisible(False)
        self.continueButton.setVisible(False)
        self.instructionsHeaderLabel.setVisible(False)
        self.bottomLabel.setVisible(False)
        self.instructionsFooterLabel.setVisible(False)
        self.MainWindow.setWindowTitle(_translate(
            "MainWindow", "GWA Toolbox Installation - Running install command.", None))
        self.cancelButton.setVisible(False)

    def startAction(self):
        self.utilities.execute_cmd(self.cmd, **self.execute_kwargs)

    def slotFinished(self):
        self.action = NEXT
        self.MainWindow.close()


class extractingWaitWindow(instructionsWindow, QtCore.QObject):

    def __init__(self, utilities, archivePath, dstPath):
        QtCore.QObject.__init__(self)

        self.utilities = utilities
        self.archivePath = archivePath
        self.dstPath = dstPath

        # Use a thread and modified QDialog to display the waiting dialog and
        # extract the files at the same time
        self.workerThread = QtCore.QThread(self)
        self.MainWindow = myQDialog(self.workerThread)
        instructionsWindow.__init__(self, self.MainWindow)

        self.utilities.moveToThread(self.workerThread)
        self.utilities.finished.connect(self.workerThread.quit)
        self.workerThread.finished.connect(self.slotFinished)
        self.workerThread.started.connect(self.startAction)

    def retranslateUi(self, MainWindow):
        super(extractingWaitWindow, self).retranslateUi(MainWindow)
        msg = (
            "Extracting an archive ({}). Please wait..."
            .format(os.path.splitext(os.path.basename(self.archivePath))[0]))
        self.topLabel.setText(_translate("MainWindow", msg, None))
        self.instructionsMainLabel.setVisible(False)
        self.continueButton.setVisible(False)
        self.instructionsHeaderLabel.setVisible(False)
        self.bottomLabel.setVisible(False)
        self.instructionsFooterLabel.setVisible(False)
        self.MainWindow.setWindowTitle(_translate(
            "MainWindow", "GWA Toolbox Installation - Extracting an archive", None))
        self.cancelButton.setVisible(False)

    def startAction(self):
        self.utilities.unzipArchive(self.archivePath, self.dstPath)

    def slotFinished(self):
        self.action = NEXT
        self.MainWindow.close()


class copyingWaitWindow(instructionsWindow, QtCore.QObject):
    def __init__(self, utilities, srcPath, dstPath, checkDstParentExists=False):
        QtCore.QObject.__init__(self)

        self.utilities = utilities
        self.srcPath = srcPath
        self.dstPath = dstPath
        self.checkDstParentExists = checkDstParentExists

        # Use a thread and modified QDialog to display the waiting dialog and
        # extract the files at the same time
        self.workerThread = QtCore.QThread(self)
        self.MainWindow = myQDialog(self.workerThread)
        instructionsWindow.__init__(self, self.MainWindow)

        self.utilities.moveToThread(self.workerThread)
        self.utilities.finished.connect(self.workerThread.quit)
        self.workerThread.finished.connect(self.slotFinished)
        self.workerThread.started.connect(self.startAction)

    def retranslateUi(self, MainWindow):
        super(copyingWaitWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate("MainWindow", "Copying files. Please wait...", None))
        self.instructionsMainLabel.setVisible(False)
        self.continueButton.setVisible(False)
        self.instructionsHeaderLabel.setVisible(False)
        self.bottomLabel.setVisible(False)
        self.instructionsFooterLabel.setVisible(False)
        self.MainWindow.setWindowTitle(_translate(
            "MainWindow", "GWA Toolbox Installation - Copying Files", None))
        self.cancelButton.setVisible(False)

    def startAction(self):
        self.utilities.copyFiles(self.srcPath, self.dstPath, self.checkDstParentExists)

    def slotFinished(self):
        self.action = NEXT
        self.MainWindow.close()


class myQDialog(QtWidgets.QDialog):
    """Reimplement QDialog to start a given thread shortly after the dialog is displayed"""

    def __init__(self, workerThread):
        super(myQDialog, self).__init__()
        self.workerThread = workerThread
        self.timer = None

    def showEvent(self, event):
        super(myQDialog, self).showEvent(event)
        self.timer = self.startTimer(200)

    def timerEvent(self, event):
        super(myQDialog, self).timerEvent(event)
        self.workerThread.start()
        if (self.timer):
            self.killTimer(self.timer)
            self.timer = None
