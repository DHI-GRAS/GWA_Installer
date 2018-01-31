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

from PyQt4 import QtCore, QtGui
from ui import welcomeDialog, installComponentDialog, postInstallComponentDialog, componentInstructionsDialog

# MACROS
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

# CONSTANTS
CANCEL = QtGui.QDialog.Rejected
NEXT = QtGui.QDialog.Accepted
SKIP = QtGui.QDialog.Accepted + 1



##################################################################################
# Parent classes
# Used to avoid overwriting the files produced by QtDesigner and pyuic4
# Mostly assign actions to buttons and set up the dialog

class installerBaseWindow():
    def __init__(self, MainWindow = None):
        if MainWindow:
            self.MainWindow = MainWindow
        else:
            self.MainWindow = QtGui.QDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("images/GWA.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8("images/GWA_logo.png")))

        QtCore.QObject.connect(self.beginButton, QtCore.SIGNAL("clicked()"), self.next)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), self.cancel)

class installWindow(installerBaseWindow, installComponentDialog.Ui_Dialog):
    def __init__(self):
        installerBaseWindow.__init__(self)
        self.setupUi(self.MainWindow)
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8("images/GWA_logo.png")))

        QtCore.QObject.connect(self.installButton, QtCore.SIGNAL("clicked()"), self.next)
        QtCore.QObject.connect(self.skipButton, QtCore.SIGNAL("clicked()"), self.skip)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), self.cancel)


class postInstallWindow(installerBaseWindow, postInstallComponentDialog.Ui_Dialog):
    def __init__(self):
        installerBaseWindow.__init__(self)
        self.setupUi(self.MainWindow)
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8("images/GWA_logo.png")))

        QtCore.QObject.connect(self.continueButton, QtCore.SIGNAL("clicked()"), self.next)
        QtCore.QObject.connect(self.skipButton, QtCore.SIGNAL("clicked()"), self.skip)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), self.cancel)
        QtCore.QObject.connect(self.dirSelectionButton, QtCore.SIGNAL("clicked()"), self.dirSelection)

    def dirSelection(self):
        path = QtGui.QFileDialog.getExistingDirectory(directory=self.dirPathText.toPlainText())
        if not path.isNull():
            self.dirPathText.setPlainText(_translate("MainWindow", path, None))

class instructionsWindow(installerBaseWindow, componentInstructionsDialog.Ui_Dialog):

    # This window can have a reimplemented QDialog used as the main window to allow
    # for multithreaded operations while the window is displayed
    def __init__(self, MainWindow = None):

        installerBaseWindow.__init__(self, MainWindow)
        self.setupUi(self.MainWindow)
        self.logoLabel.setPixmap(QtGui.QPixmap(_fromUtf8("images/GWA_logo.png")))

        QtCore.QObject.connect(self.continueButton, QtCore.SIGNAL("clicked()"), self.next)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), self.cancel)


###############################################################################
# Child classes
# Individualise the parent classes mostly by changing the text


# Instructions for activating GWA Toolbox plugins
class uninstallInstructionsWindow(instructionsWindow):
    def __init__(self):
        instructionsWindow.__init__(self)

    def retranslateUi(self, MainWindow):
        super(uninstallInstructionsWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate("MainWindow", "For smooth installation process some of the old components of GWA Toolbox have to be uninstalled if they are present on your computer.", None))
        self.instructionsMainLabel.setText(_translate("MainWindow", "Please follow the uninstallation instructions present in the 'GWA Toolbox installation' document located in the GWA Toolbox installation directory.", None))
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Uninstall old version", None))


# OSGeo4W
class osgeo4wInstallWindow(installWindow):
    def __init__(self):
        installWindow.__init__(self)
        self.componentLogoLabel.setPixmap(QtGui.QPixmap(_fromUtf8("images/osgeo4wLogo.png")))

    def retranslateUi(self, MainWindow):
        super(osgeo4wInstallWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate("MainWindow", "QGIS is the main GUI used by GWA Toolbox while Orfeo Toolbox and GRASS GIS provide many of the commonly used data processing functions. They are installed together through the OSGeo4W installer.", None))
        self.instructionMainLabel.setText(_translate("MainWindow", "After clicking on the \"Install\" button the OSGeo4W installer will start. The process should be automatic but if any question dialogs pop-up just click OK.", None))
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Install QGIS, Orfeo Toolbox and GRASS GIS", None))

class osgeo4wPostInstallWindow(postInstallWindow):
    def __init__(self, defaultPath):
        self.defaultPath = defaultPath
        postInstallWindow.__init__(self)
        self.componentLogoLabel.setPixmap(QtGui.QPixmap(_fromUtf8("images/osgeo4wLogo.png")))

    def retranslateUi(self, MainWindow):
        super(osgeo4wPostInstallWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate("MainWindow", "QGIS is the main GUI used by GWA Toolbox while Orfeo Toolbox and GRASS GIS provide many of the commonly used data processing functions. They are installed together through the OSGeo4W installer.", None))
        self.instructionsMainLabel.setText(_translate("MainWindow", "The GWA Toolbox installer will now perform additional post installation tasks for QGIS (activating plugins, copying extra libraries, etc.). If you changed the OSGeo4W/QGIS installation directory during the previous step (or skipped the step), make sure that you check the path to the directory below and update it if necessary.", None))
        self.dirPathText.setPlainText(_translate("MainWindow", self.defaultPath, None))
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Install QGIS, Orfeo Toolbox and GRASS GIS", None))


# BEAM
class beamInstallWindow(installWindow):
    def __init__(self):
        installWindow.__init__(self)
        self.componentLogoLabel.setPixmap(QtGui.QPixmap(_fromUtf8("images/beamLogo.png")))

    def retranslateUi(self, MainWindow):
        super(beamInstallWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate("MainWindow", "BEAM is a software for analyzing optical and thermal data derived with satellites operated by European Space Agency (ESA) and other organisation.", None))
        self.instructionMainLabel.setText(_translate("MainWindow", "After clicking on the \"Install\" button the BEAM installer will start. In the installer you will be asked to accept the BEAM license conditions followed by a couple of installation questions. In all the questions you can keep the default answers by clicking \"Next >\" until the installation starts.", None))
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Install BEAM", None))

class beamPostInstallWindow(postInstallWindow):
    def __init__(self, defaultPath):
        self.defaultPath = defaultPath
        postInstallWindow.__init__(self)
        self.componentLogoLabel.setPixmap(QtGui.QPixmap(_fromUtf8("images/beamLogo.png")))

    def retranslateUi(self, MainWindow):
        super(beamPostInstallWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate("MainWindow", "BEAM is a software for analyzing optical and thermal data derived with satellites operated by European Space Agency (ESA) and other organisation.", None))
        self.instructionsMainLabel.setText(_translate("MainWindow", "The GWA Toolbox installer will now perform additional post installation tasks for BEAM (activating plugins, copying extra libraries, etc.). If you changed the BEAM installation directory during the previous step (or skipped the step), make sure that you check the path to the directory below and update it if necessary.", None))
        self.dirPathText.setPlainText(_translate("MainWindow", self.defaultPath, None))
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Install BEAM", None))

# SNAP
class snapInstallWindow(installWindow):
    def __init__(self):
        installWindow.__init__(self)
        self.componentLogoLabel.setPixmap(QtGui.QPixmap(_fromUtf8("images/snapLogo.png")))

    def retranslateUi(self, MainWindow):
        super(snapInstallWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate("MainWindow", "Snap Toolbox is a software for analyzing data derived with satellites operated by European Space Agency (ESA) and other organisation.", None))
        self.instructionMainLabel.setText(_translate("MainWindow", "After clicking on the \"Install\" button the Snap Toolbox installer will start. In the installer you will be asked to accept the Snap Toolbox license conditions followed by a couple of installation questions. In all the questions you can keep the default answers by clicking \"Next >\" until the installation starts.", None))
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Install Snap Toolbox", None))

class snapPostInstallWindow(postInstallWindow):
    def __init__(self, defaultPath):
        self.defaultPath = defaultPath
        postInstallWindow.__init__(self)
        self.componentLogoLabel.setPixmap(QtGui.QPixmap(_fromUtf8("images/snapLogo.png")))

    def retranslateUi(self, MainWindow):
        super(snapPostInstallWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate("MainWindow", "Snap Toolbox is a software for analyzing data derived with satellites operated by European Space Agency (ESA) and other organisation.", None))
        self.instructionsMainLabel.setText(_translate("MainWindow", "The GWA Toolbox installer will now perform additional post installation tasks for Snap Toolbox (activating plugins, copying extra libraries, etc.). If you changed the Snap Toolbox installation directory during the previous step (or skipped the step), make sure that you check the path to the directory below and update it if necessary.", None))
        self.dirPathText.setPlainText(_translate("MainWindow", self.defaultPath, None))
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Install Snap Toolbox", None))

# R
class rInstallWindow(installWindow):
    def __init__(self):
        installWindow.__init__(self)
        self.componentLogoLabel.setPixmap(QtGui.QPixmap(_fromUtf8("images/rLogo.png")))

    def retranslateUi(self, MainWindow):
        super(rInstallWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate("MainWindow", "R is a statistical scripting language used by GWA Toolbox for various data processing tasks.", None))
        self.instructionMainLabel.setText(_translate("MainWindow", "After clicking on the \"Install\" button the OSGeo4W installer will start. In the installer you will be asked to accept the R license conditions followed by a couple of installation questions. In all the questions you can keep the default answers by clicking \"Next >\" until the installation starts.", None))
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Install R", None))

class rPostInstallWindow(postInstallWindow):
    def __init__(self, defaultPath):
        self.defaultPath = defaultPath
        postInstallWindow.__init__(self)
        self.componentLogoLabel.setPixmap(QtGui.QPixmap(_fromUtf8("images/rLogo.png")))

    def retranslateUi(self, MainWindow):
        super(rPostInstallWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate("MainWindow", "R is a statistical scripting language used by GWA Toolbox for various data processing tasks.", None))
        self.instructionsMainLabel.setText(_translate("MainWindow", "The GWA Toolbox installer will now perform additional post installation tasks for R (activating plugins, copying extra libraries, etc.). If you changed the R installation directory during the previous step (or skipped the step), make sure that you check the path to the directory below and update it if necessary.", None))
        self.dirPathText.setPlainText(_translate("MainWindow", self.defaultPath, None))
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Install R", None))

# PostGre
class postgreInstallWindow(installWindow):
    def __init__(self):
        installWindow.__init__(self)
        self.componentLogoLabel.setPixmap(QtGui.QPixmap(_fromUtf8("images/postgisLogo.png")))

    def retranslateUi(self, MainWindow):
        super(postgreInstallWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate("MainWindow", "PostGIS is a geospatial database used by GWA Toolbox for storing certain types of data. It is not necessary to have it installed on every computer using GWA Toolbox, since the database can run from a central server. Therefore its installation is optional.", None))
        self.instructionMainLabel.setText(_translate("MainWindow", "After clicking on the \"Install\" button the PostgreSQL (PostGIS back-end) installer will start. You can keep all the default options and set superuser password (e.g. waterinfo) when requested. <b>Remember to write down the superuser name and the password.</b> In the last step make sure that the option to launch Stack Builder is <b>NOT</b> selected.", None))
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Install PostGIS (Optional)", None))

# PostGIS
class postgisInstallWindow(installWindow):
    def __init__(self):
        installWindow.__init__(self)
        self.componentLogoLabel.setPixmap(QtGui.QPixmap(_fromUtf8("images/postgisLogo.png")))

    def retranslateUi(self, MainWindow):
        super(postgisInstallWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate("MainWindow", "PostGIS is a geospatial database used by GWA Toolbox for storing certain types of data. It is not necessary to have it installed on every computer using GWA Toolbox, since the database can run from a central server. Therefore its installation is optional.", None))
        self.instructionMainLabel.setText(_translate("MainWindow", "After clicking on the \"Install\" button the PostGIS installer will start. You need to accept the license and then when choosing components to install select 'PostGIS' <b>but not 'Create spatial database'</b>. If any questions pop up just click Yes.", None))
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Install PostGIS (Optional)", None))

# Budyko Hydrological Model
class budykoInstallWindow(installWindow):
    def __init__(self):
        installWindow.__init__(self)
        self.componentLogoLabel.setPixmap(QtGui.QPixmap(_fromUtf8("images/GWA_logo.png")))

    def retranslateUi(self, MainWindow):
        super(snapInstallWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate("MainWindow", "The Budyko Hydrological Model is used to simulate hydrological processes.", None))
        self.instructionMainLabel.setText(_translate("MainWindow", "The installation of Windows MPI and other dependencies requires no user interaction. Just click \"Continue\".", None))
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Install Budyko Hydrological Model", None))


# Finish
class finishWindow(instructionsWindow):
    def __init__(self):
        instructionsWindow.__init__(self)

    def retranslateUi(self, MainWindow):
        super(finishWindow, self).retranslateUi(MainWindow)
        self.topLabel.setText(_translate("MainWindow", "The GWA Toolbox has now been installed on your computer. Thank you.", None))
        self.instructionsMainLabel.setText(_translate("MainWindow", "You can now start QGIS to begin working with the GWA Toolbox.", None))
        self.continueButton.setVisible(False)
        self.instructionsHeaderLabel.setVisible(False)
        self.bottomLabel.setVisible(False)
        self.instructionsFooterLabel.setText(_translate("MainWindow", "Click \"Finish\" to finish the installation process", None))
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Finished", None))
        self.cancelButton.setText(_translate("MainWindow", "Finish", None))


# cmd please wait
class cmdWaitWindow(instructionsWindow, QtCore.QObject):

    def __init__(self, utilities, cmd):
        QtCore.QObject.__init__(self)

        self.utilities = utilities
        self.cmd = cmd

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
        self.topLabel.setText(_translate("MainWindow", "Running an external install command. Please wait...", None))
        self.instructionsMainLabel.setVisible(False)
        self.continueButton.setVisible(False)
        self.instructionsHeaderLabel.setVisible(False)
        self.bottomLabel.setVisible(False)
        self.instructionsFooterLabel.setVisible(False)
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Running install command.", None))
        self.cancelButton.setVisible(False)

    def startAction(self):
        self.utilities.execute_cmd(self.cmd)

    def slotFinished(self):
        self.action = NEXT
        self.MainWindow.close()


# Extracting please wait
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
        self.topLabel.setText(_translate("MainWindow", "Extracting an archive. Please wait...", None))
        self.instructionsMainLabel.setVisible(False)
        self.continueButton.setVisible(False)
        self.instructionsHeaderLabel.setVisible(False)
        self.bottomLabel.setVisible(False)
        self.instructionsFooterLabel.setVisible(False)
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Extracting an archive", None))
        self.cancelButton.setVisible(False)

    def startAction(self):
        self.utilities.unzipArchive(self.archivePath, self.dstPath)

    def slotFinished(self):
        self.action = NEXT
        self.MainWindow.close()

# Copying please wait
class copyingWaitWindow(instructionsWindow, QtCore.QObject):
    def __init__(self, utilities, srcPath, dstPath, checkDstParentExists = False):
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
        self.MainWindow.setWindowTitle(_translate("MainWindow", "GWA Toolbox Installation - Copying Files", None))
        self.cancelButton.setVisible(False)

    def startAction(self):
        self.utilities.copyFiles(self.srcPath, self.dstPath, self.checkDstParentExists)

    def slotFinished(self):
        self.action = NEXT
        self.MainWindow.close()

# Reimplement QDialog to start a given thread shortly after the dialog is displayed
class myQDialog(QtGui.QDialog):

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
