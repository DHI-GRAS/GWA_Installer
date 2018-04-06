import os
import sys
import glob
import time
import errno
import shutil
import functools
import subprocess
import traceback
import tempfile
import datetime
import logging
from zipfile import ZipFile
from distutils import dir_util

from PyQt4 import QtCore, QtGui
from installerGUI import installerWelcomeWindow
from installerGUI import osgeo4wInstallWindow, osgeo4wPostInstallWindow
from installerGUI import beamInstallWindow, beamPostInstallWindow
from installerGUI import snapInstallWindow, snapPostInstallWindow
from installerGUI import rInstallWindow, rPostInstallWindow
from installerGUI import postgreInstallWindow, postgisInstallWindow
from installerGUI import mapwindowInstallWindow
from installerGUI import mwswatInstallWindow, mwswatPostInstallWindow, swateditorInstallWindow
from installerGUI import extractingWaitWindow, copyingWaitWindow
from installerGUI import cmdWaitWindow
from installerGUI import uninstallInstructionsWindow
from installerGUI import finishWindow
from installerGUI import CANCEL, SKIP, NEXT

import installer_utils

logger = logging.getLogger('gwa_installer')


def _set_logfile_handler():
    datestr = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    logfile = os.path.join(tempfile.gettempdir(), 'gwa_install_{}.log'.format(datestr))
    logger.setLevel('DEBUG')
    fh = logging.FileHandler(logfile)
    fh.setLevel('DEBUG')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logfile


class Installer():

    def __init__(self, logfile):
        self.util = Utilities(logfile)

    def runInstaller(self):
        ########################################################################
        # welcome window with license
        self.dialog = installerWelcomeWindow()
        res = self.showDialog()

        if res == NEXT:
            # select installation files for 32 or 64 bit install
            installationsDirs = ['Installations_x32', 'Installations_x64']
            if os.path.isdir(installationsDirs[0]):
                is32bit = True
                installationsDir = installationsDirs[0]
                _joinbindir = functools.partial(os.path.join, installationsDir)
                osgeo4wInstall = _joinbindir("osgeo4w-setup.bat")
                beamInstall = _joinbindir("beam_5.0_win32_installer.exe")
                snapInstall = _joinbindir("esa-snap_sentinel_windows_6_0.exe")
                rInstall = _joinbindir("R-3.3.2-win.exe")
                postgreInstall = _joinbindir("postgresql-10.2-1-windows.exe")
                postgisInstall = _joinbindir("postgis-bundle-pg10x32-setup-2.4.3-1.exe")
                mapwindowInstall = _joinbindir("MapWindowx86Full-v488SR-installer.exe")
                mwswatInstall = _joinbindir("MWSWAT2009.exe")
                swateditorInstall = "MWSWAT additional software\\SwatEditor_Install\\Setup.exe"
            elif os.path.isdir(installationsDirs[1]):
                is32bit = False
                installationsDir = installationsDirs[1]
                _joinbindir = functools.partial(os.path.join, installationsDir)
                osgeo4wInstall = _joinbindir("osgeo4w-setup.bat")
                beamInstall = _joinbindir("beam_5.0_win64_installer.exe")
                snapInstall = _joinbindir("esa-snap_sentinel_windows-x64_6_0.exe")
                rInstall = _joinbindir("R-3.3.2-win.exe")
                postgreInstall = _joinbindir("postgresql-10.2-1-windows-x64.exe")
                postgisInstall = _joinbindir("postgis-bundle-pg10x64-setup-2.4.3-1.exe")
                mapwindowInstall = _joinbindir("MapWindowx86Full-v488SR-installer.exe")
                mwswatInstall = _joinbindir("MWSWAT2009.exe")
                swateditorInstall = "MWSWAT additional software\\SwatEditor_Install\\Setup.exe"
            else:
                self.util.error_exit(
                    'Neither 32 bit nor 64 bit instalations directory exists. '
                    'Package incomplete.')
                return
            # select default installation directories for 32 or 64 bit install
            if is32bit:
                install_dirs = {
                    'osgeo4w': "C:\\OSGeo4W",
                    'snap': "C:\\Program Files\\snap",
                    'beam': "C:\\Program Files\\beam-5.0",
                    'r': "C:\\Program Files\\R\\R-3.3.2",
                    'mapwindow': "C:\\Program Files\\MapWindow",
                }
            else:
                install_dirs = {
                    'osgeo4w': "C:\\OSGeo4W64",
                    'snap': "C:\\Program Files\\snap",
                    'beam': "C:\\Program Files\\beam-5.0",
                    'r': "C:\\Program Files\\R\\R-3.3.2",
                    'mapwindow': "C:\\Program Files (x86)\\MapWindow"}

        elif res == CANCEL:
            del self.dialog
            return
        else:
            self.unknownActionPopup()

        ########################################################################
        # Information about uninstalling old version
        self.dialog = uninstallInstructionsWindow()
        res = self.showDialog()
        if res == CANCEL:
            del self.dialog
            return

        ########################################################################
        # Install OSGeo4W (QGIS, OTB, SAGA, GRASS)

        self.dialog = osgeo4wInstallWindow()
        res = self.showDialog()

        # run the OSGeo4W installation here as an outside process
        if res == NEXT:
            self.util.execSubprocess(osgeo4wInstall)
        elif res == SKIP:
            pass
        elif res == CANCEL:
            del self.dialog
            return
        else:
            self.unknownActionPopup()

        # ask for post-installation even if user has skipped installation
        self.dialog = osgeo4wPostInstallWindow(install_dirs['osgeo4w'])
        res = self.showDialog()

        # copy plugins, scripts, and models and activate processing providers
        if res == NEXT:
            install_dirs['osgeo4w'] = str(self.dialog.dirPathText.toPlainText())

            # copy the plugins
            dstPath = os.path.join(os.path.expanduser("~"), ".qgis2", "python", 'plugins')
            srcPath = os.path.join("QGIS additional software", "plugins", "plugins.zip")
            # try to delete old plugins before copying the new ones to avoid conflicts
            plugins_to_delete = [
                'mikecprovider',
                'processing',
                'processing_gpf',
                'photo2shape',
                'processing_workflow',
                'openlayers_plugin',
                'pointsamplingtool',
                'temporalprofiletool',
                'valuetool']
            for plugin in plugins_to_delete:
                self.util.deleteDir(
                    os.path.join(dstPath, plugin))
            self.dialog = extractingWaitWindow(self.util, srcPath, dstPath)
            self.showDialog()

            # copy scripts and models
            QGIS_extras_dir = os.path.abspath("QGIS additional software")
            processing_dir = os.path.join(os.path.expanduser("~"), ".qgis2", "processing")
            processing_packages = glob.glob(os.path.join(QGIS_extras_dir, '*.zip'))
            logger.info('Found processing packages: %s', processing_packages)
            for zipfname in processing_packages:
                # show dialog because it might take some time on slower computers
                self.dialog = extractingWaitWindow(self.util, zipfname, processing_dir)
                self.showDialog()

            # copy additional python packages
            site_packages_dir = os.path.join(
                install_dirs['osgeo4w'], 'apps', 'Python27', 'Lib', 'site-packages')
            python_packages = glob.glob(os.path.join(QGIS_extras_dir, 'python_packages', '*.zip'))
            logger.info('Found python packages: %s', python_packages)
            for zipfname in python_packages:
                self.dialog = extractingWaitWindow(self.util, zipfname, site_packages_dir)
                self.showDialog()

            # install additional python packages with pip
            pip_package_dir = os.path.join(QGIS_extras_dir, 'python_packages_pip')
            self.util.install_pip_offline(
                osgeo_root=install_dirs['osgeo4w'],
                package_dir=pip_package_dir)

            # activate plugins and processing providers
            self.util.activatePlugins()
            self.util.activateProcessingProviders(install_dirs['osgeo4w'])
        elif res == SKIP:
            pass
        elif res == CANCEL:
            del self.dialog
            return
        else:
            self.unknownActionPopup()

        # #######################################################################
        # Install BEAM

        self.dialog = beamInstallWindow()
        res = self.showDialog()

        # run the BEAM installation here as an outside process
        if res == NEXT:
            self.util.execSubprocess(beamInstall)
            # self.dialog =  beamPostInstallWindow(install_dirs['beam']);
            # res = self.showDialog()
        elif res == SKIP:
            pass
        elif res == CANCEL:
            del self.dialog
            return
        else:
            self.unknownActionPopup()

        # ask for post-installation even if user has skipped installation
        self.dialog = beamPostInstallWindow(install_dirs['beam'])
        res = self.showDialog()

        # copy the additional BEAM modules and set the amount of memory to be used with GPT
        if res == NEXT:
            dirPath = install_dirs['beam'] = str(self.dialog.dirPathText.toPlainText())
            dstPath = os.path.join(dirPath, "modules")
            srcPath = "BEAM additional modules"
            self.dialog = copyingWaitWindow(self.util, srcPath, dstPath)
            self.showDialog()
            # 32 bit systems usually have less RAM so assign less to BEAM
            ram_fraction = 0.4 if is32bit else 0.6
            try:
                installer_utils.modifyRamInBatFiles(
                    os.path.join(dirPath, "bin", 'gpt.bat'), ram_fraction)
            except IOError as exc:
                self.util.error_exit(str(exc))
            self.util.activateBEAMplugin(dirPath)
        elif res == SKIP:
            pass
        elif res == CANCEL:
            del self.dialog
            return
        else:
            self.unknownActionPopup()

        ########################################################################
        # Install Snap Toolbox

        self.dialog = snapInstallWindow()
        res = self.showDialog()

        # run the Snap installation here as an outside process
        if res == NEXT:
            self.util.execSubprocess(snapInstall)
        elif res == SKIP:
            pass
        elif res == CANCEL:
            del self.dialog
            return
        else:
            self.unknownActionPopup()

        # ask for post-installation even if user has skipped installation
        self.dialog = snapPostInstallWindow(install_dirs['snap'])
        res = self.showDialog()

        # Set the amount of memory to be used with NEST GPT
        if res == NEXT:
            install_dirs['snap'] = str(self.dialog.dirPathText.toPlainText())
            site_packages_dir = os.path.join(
                install_dirs['osgeo4w'], 'apps', 'Python27', 'Lib', 'site-packages')
            # configure snappy
            confbat = os.path.join(install_dirs['snap'], 'bin', 'snappy-conf.bat')
            osgeopython = os.path.join(install_dirs['osgeo4w'], 'bin', 'python.exe')
            cmd = [confbat, osgeopython, site_packages_dir]
            self.dialog = cmdWaitWindow(self.util, cmd, notify=True)
            self.showDialog()

            snappy_ini = os.path.join(site_packages_dir, 'snappy.ini')
            with open(snappy_ini, 'w') as f:
                f.write(
                    '[DEFAULT]\n'
                    'snap_home: {}\n'
                    .format(install_dirs['snap']))

            jpyconfig = os.path.join(site_packages_dir, 'jpyconfig.py')
            replace = {
                'java_home': '"{}"'.format(os.path.join(install_dirs['snap'], 'jre')),
                'jvm_dll': 'None'}
            installer_utils.fix_jpyconfig(jpyconfig, replace=replace)

            # 32 bit systems usually have less RAM so assign less to S1 Toolbox
            ram_fraction = 0.4 if is32bit else 0.6
            settingsfile = os.path.join(install_dirs['snap'], 'bin', 'gpt.vmoptions')
            try:
                installer_utils.modifyRamInBatFiles(settingsfile, ram_fraction)
            except IOError as exc:
                self.util.error_exit(str(exc))
            # There is a bug in snap installer so the gpt file has to be
            # modified for 32 bit installation
            if is32bit:
                try:
                    installer_utils.removeIncompatibleJavaOptions(settingsfile)
                except IOError as exc:
                    self.error_exit(str(exc))
            self.util.activateSNAPplugin(install_dirs['snap'])
        elif res == SKIP:
            pass
        elif res == CANCEL:
            del self.dialog
            return
        else:
            self.unknownActionPopup()

        # #######################################################################
        # Install R

        self.dialog = rInstallWindow()
        res = self.showDialog()

        # run the R installation here as an outside process
        if res == NEXT:
            self.util.execSubprocess(rInstall)
            # self.dialog = rPostInstallWindow(install_dirs['r'])
            # res = self.showDialog()
        elif res == SKIP:
            pass
        elif res == CANCEL:
            del self.dialog
            return
        else:
            self.unknownActionPopup()

        # ask for post-installation even if user has skipped installation
        self.dialog = rPostInstallWindow(install_dirs['r'])
        res = self.showDialog()

        # Copy the R additional libraries
        if res == NEXT:
            dirPath = install_dirs['r'] = str(self.dialog.dirPathText.toPlainText())
            dstPath = os.path.join(dirPath, "library")
            srcPath = "R additional libraries"
            # show dialog because it might take some time on slower computers
            self.dialog = extractingWaitWindow(
                self.util, os.path.join(srcPath, "libraries.zip"), dstPath)
            self.showDialog()
            if is32bit:
                self.util.activateRplugin(dirPath, "false")
            else:
                self.util.activateRplugin(dirPath, "true")
        elif res == SKIP:
            pass
        elif res == CANCEL:
            del self.dialog
            return
        else:
            self.unknownActionPopup()

        ########################################################################
        # Install PostGIS
        postgres_installed = False

        self.dialog = postgreInstallWindow()
        res = self.showDialog()

        # install Postgres
        if res == NEXT:
            self.util.execSubprocess(postgreInstall)
            postgres_installed = True
        elif res == SKIP:
            pass
        elif res == CANCEL:
            del self.dialog
            return
        else:
            self.unknownActionPopup()

        if postgres_installed:
            # install PostGIS
            self.dialog = postgisInstallWindow()
            res = self.showDialog()
            if res == NEXT:
                self.util.execSubprocess(postgisInstall)
            elif res == SKIP:
                pass
            elif res == CANCEL:
                del self.dialog
                return
            else:
                self.unknownActionPopup()

        ########################################################################
        # Install MapWindow, SWAT and PEST
        mapwindow_installed = False
        mswat_installed = False
        swateditor_installed = False

        # install MapWindow
        self.dialog = mapwindowInstallWindow()
        res = self.showDialog()
        if res == NEXT:
            self.util.execSubprocess(mapwindowInstall)
            mapwindow_installed = True
        elif res == SKIP:
            pass
        elif res == CANCEL:
            del self.dialog
            return
        else:
            self.unknownActionPopup()

        if mapwindow_installed:
            # install MS SWAT
            self.dialog = mwswatInstallWindow()
            res = self.showDialog()
            if res == NEXT:
                self.util.execSubprocess(mwswatInstall)
                mswat_installed = True
            elif res == SKIP:
                pass
            elif res == CANCEL:
                del self.dialog
                return
            else:
                self.unknownActionPopup()

        if mswat_installed:
            # install SWAT editor
            self.dialog = swateditorInstallWindow()
            res = self.showDialog()
            if res == NEXT:
                self.util.execSubprocess(swateditorInstall)
                time.sleep(5)
                swateditor_installed = True
            elif res == SKIP:
                pass
            elif res == CANCEL:
                del self.dialog
                return
            else:
                self.unknownActionPopup()

        if swateditor_installed:
            # install SWAT post-installation stuff
            self.dialog = mwswatPostInstallWindow(install_dirs['mapwindow'])
            res = self.showDialog()
            if res == NEXT:
                # copy the DTU customised MWSWAT 2009 installation
                install_dirs['mapwindow'] = dirPath = str(self.dialog.dirPathText.toPlainText())
                mwswatPath = os.path.join(dirPath, "Plugins", "MWSWAT2009")
                dstPath = os.path.join(mwswatPath, 'swat2009DtuEnvVers0.2')
                srcPath = "MWSWAT additional software\\swat2009DtuEnvVers0.2"
                self.dialog = copyingWaitWindow(self.util, srcPath, dstPath)
                self.showDialog()

                # copy and rename the customised MWSWAT exe
                oldexe = os.path.join(mwswatPath, "swat2009rev481.exe_old")
                revexe = os.path.join(mwswatPath, "swat2009rev481.exe")
                newexe = os.path.join(dstPath, "swat2009DtuEnv.exe")

                if os.path.isfile(oldexe):
                    os.remove(oldexe)
                os.rename(revexe, oldexe)

                self.util.copyFiles(newexe, mwswatPath)
                if os.path.isfile(revexe):
                    os.remove(revexe)
                os.rename(newexe, revexe)

                # copy the modified database file
                self.util.copyFiles("MWSWAT additional software\\mwswat2009.mdb", mwswatPath)
                # copy PEST
                self.dialog = copyingWaitWindow(
                    self.util, "MWSWAT additional software\\PEST",
                    os.path.join(mwswatPath, "PEST"))
                self.showDialog()
                # activate the plugin
                self.util.activateSWATplugin(dirPath)
            elif res == SKIP:
                pass
            elif res == CANCEL:
                del self.dialog
                return
            else:
                self.unknownActionPopup()

        # Finish
        self.dialog = finishWindow()
        self.showDialog()
        del self.dialog

    def showDialog(self):
        return(self.dialog.exec_())

    def unknownActionPopup(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(
            "Unknown action chosen in the previous installation step. "
            "Ask the developer to check the installation script!\n\n Quitting installation")
        msgBox.exec_()


##########################################
# helper functions

class Utilities(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    def __init__(self, logfile):

        QtCore.QObject.__init__(self)
        # QGIS and processing settings
        self.qsettings = QtCore.QSettings("QGIS", "QGIS2")
        # logging
        self.logfile = logfile

    def _log_traceback(self, notify=False, fail=False):
        logger.exception('Something went wrong.')
        if fail:
            raise
        elif notify:
            trace = traceback.format_exc()
            msgBox = QtGui.QMessageBox()
            msgBox.setText(
                "An error occurred: {}. Log written to \'{}\'."
                .format(trace, self.logfile))
            msgBox.exec_()

    def execSubprocess(self, command):
        logger.info('Running binary installer: %s', command)
        # command should be a path to an exe file so check if it exists
        if not os.path.isfile(command):
            msgBox = QtGui.QMessageBox()
            msgBox.setText(
                "Could not find the installation file for this component!\n\n "
                "Skipping to next component")
            msgBox.exec_()
            # self.dialog.action = SKIP
            return

        proc = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True).stdout
        for line in iter(proc.readline, ""):
            pass

    def execute_cmd(self, cmd, shell=False, notify=False):
        """Execute cmd and save output to log file"""
        logger.info('Executing command: %s', cmd)
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            output = subprocess.check_output(
                cmd,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=si,
                shell=shell)
            logger.info(output)
        except subprocess.CalledProcessError:
            self._log_traceback(notify=notify)
        finally:
            self.finished.emit()

    def install_msi(self, msipath):
        logfname = os.path.splitext(os.path.basename(msipath))[0] + '_gwa_install.log'
        logpath = os.path.join(tempfile.gettempdir(), logfname)
        logger.info('Installing MSI %s and logging to %s', msipath, logpath)
        cmd = 'msiexec /passive /norestart /i {msipath} /log {logpath}'.format(msipath, logpath)
        self.dialog = cmdWaitWindow(self.util, cmd, shell=True, notify=True)
        self.showDialog()

    def install_pip_offline(self, osgeo_root, package_dir):
        requirements_file = os.path.join(package_dir, 'requirements.txt')
        logger.info('Installing with pip install -r %s', requirements_file)
        if not os.path.isfile(requirements_file):
            self.error_exit('No requirements file found in {}'.format(requirements_file))
        osgeo_envbat = os.path.join(osgeo_root, 'bin', 'o4w_env.bat')
        if not os.path.isfile(osgeo_envbat):
            raise self.error_exit('No OSGeo env bat file found in {}'.format(osgeo_envbat))
        cmd = (
            'call {osgeo_envbat} & '
            'if defined OSGEO4W_ROOT '
            '('
            'python -m pip install --no-index --find-links "{package_dir}" '
            '-r "{requirements_file}"'
            ')'
            .format(
                osgeo_envbat=osgeo_envbat,
                package_dir=package_dir,
                requirements_file=requirements_file))

        self.dialog = cmdWaitWindow(self.util, cmd, shell=True, notify=True)
        self.showDialog()

    def deleteFile(self, filePath):
        logger.info('Deleting file %s', filePath)
        try:
            os.remove(filePath)
        except OSError:
            self._log_traceback(notify=False)

    def deleteDir(self, dirPath):
        logger.info('Deleting dir %s', dirPath)
        try:
            shutil.rmtree(dirPath, ignore_errors=True)
        except OSError:
            self._log_traceback(notify=False)

    def error_exit(self, msg):
        logger.error(msg)
        msgBox = QtGui.QMessageBox()
        msgBox.setText(msg)
        msgBox.exec_()
        self.finished.emit()

    def copyFiles(self, srcPath, dstPath, checkDstParentExists=True):
        logger.info('Copying files from %s to %s', srcPath, dstPath)

        # a simple check to see if we are copying to the right directory by making sure that
        # its parent exists
        if checkDstParentExists:
            if not os.path.isdir(os.path.dirname(dstPath)):
                self.error_exit(
                    "Could not find the destination directory!\n\n "
                    "No files were copied.")
                return

        # checkWritePremissions alsoe creates the directory if it doesn't exist yet
        if not self.checkWritePermissions(dstPath):
            self.error_exit(
                "You do not have permissions to write to destination directory!\n\n "
                "No files were copied.\n\n"
                "Re-run the installer with administrator privileges or manually "
                "copy files from {} to {} to  after the installation process is over."
                .format(srcPath, dstPath))
            return

        # for directories copy the whole directory recursively
        if os.path.isdir(srcPath):
            dir_util.copy_tree(srcPath, dstPath)
        # for files create destination directory is necessary and copy the file
        elif os.path.isfile(srcPath):
            shutil.copy(srcPath, dstPath)
        else:
            msg = "Cannot find the source directory!\n\n No files were copied."
            logger.error(msg)
            msgBox = QtGui.QMessageBox()
            msgBox.setText(msg)
            msgBox.exec_()

        self.finished.emit()

    def unzipArchive(self, archivePath, dstPath):
        logger.info('Unzipping %s to %s', archivePath, dstPath)
        if not os.path.isfile(archivePath):
            self.error_exit("Could not find the archive!\n\n No files were extracted.")
            return

        # checkWritePremissions also creates the directory if it doesn't exist yet
        if not self.checkWritePermissions(dstPath):
            self.error_exit(
                "You do not have permissions to write to destination directory!\n\n "
                "No files were copied.\n\n" +
                "Re-run the installer with administrator privileges or manually unzip "
                "files from {} to {} to after the installation process is over."
                .format(archivePath, dstPath))
            return

        with ZipFile(archivePath) as archive:
            archive.extractall(dstPath)
        self.finished.emit()

    def checkWritePermissions(self, dstPath):
        logger.debug('Checking write permissions on %s', dstPath)
        testfile = os.path.join(dstPath, "_test")
        try:
            if not os.path.isdir(dstPath):
                logger.debug('Creating directory in %s', dstPath)
                os.makedirs(dstPath)
            with open(testfile, 'w'):
                pass
        except IOError as e:
            logger.debug('%s', e)
            if e.errno == errno.EACCES:
                return False
            else:
                return False
        else:
            try:
                os.remove(testfile)
            except:
                pass
        return True

    def setQGISSettings(self, name, value):
        logger.info('Set %s to %s', name, value)
        self.qsettings.setValue(name, value)

    def activateThis(self, *names):
        # sets the requested option(s) to 'true'
        for name in names:
            self.setQGISSettings(name, 'true')

    def activatePlugins(self):
        self.activateThis(
                "PythonPlugins/atmospheric_correction",
                "PythonPlugins/processing_workflow",
                "PythonPlugins/processing_SWAT",
                "PythonPlugins/openlayers_plugin",
                "PythonPlugins/photo2shape",
                "PythonPlugins/pointsamplingtool",
                "PythonPlugins/processing",
                "PythonPlugins/temporalprofiletool",
                "PythonPlugins/valuetool",
                "plugins/zonalstatisticsplugin")

    def activateProcessingProviders(self, osgeodir):
        self.setQGISSettings("Processing/configuration/ACTIVATE_GRASS70", "true")
        self.setQGISSettings("Processing/configuration/ACTIVATE_GRASS", "true")
        self.activateThis(
                "Processing/configuration/ACTIVATE_MODEL",
                "Processing/configuration/ACTIVATE_OTB",
                "Processing/configuration/ACTIVATE_QGIS",
                "Processing/configuration/ACTIVATE_SAGA",
                "Processing/configuration/ACTIVATE_DHIGRAS",
                "Processing/configuration/ACTIVATE_SCRIPT",
                "Processing/configuration/ACTIVATE_WORKFLOW",
                "Processing/configuration/ACTIVATE_GWA_TBX",
                "Processing/configuration/ACTIVATE_WOIS_TOOLBOX",
                "Processing/configuration/ACTIVATE_WG9HM",
                "Processing/configuration/GRASS_LOG_COMMANDS",
                "Processing/configuration/GRASS_LOG_CONSOLE",
                "Processing/configuration/SAGA_LOG_COMMANDS",
                "Processing/configuration/SAGA_LOG_CONSOLE",
                "Processing/configuration/USE_FILENAME_AS_LAYER_NAME",
                "Processing/configuration/TASKBAR_BUTTON_GWA_TBX")
        self.setQGISSettings("Processing/configuration/TASKBAR_BUTTON_WORKFLOW", "false")
        # GRASS_FOLDER depends on GRASS version and must be set explicitly here
        try:
            grass_root = os.path.join(osgeodir, 'apps', 'grass')
            grass_folders = sorted([
                d for d in glob.glob(os.path.join(grass_root, 'grass-*'))
                if os.path.isdir(d)])
            grassFolder = grass_folders[-1]
            self.setQGISSettings("Processing/configuration/GRASS_FOLDER", grassFolder)
        except (IndexError, OSError):
            pass

    def activateBEAMplugin(self, dirPath):
        self.activateThis(
                "PythonPlugins/processing_gpf",
                "Processing/configuration/ACTIVATE_BEAM")
        self.setQGISSettings("Processing/configuration/BEAM_FOLDER", dirPath)

    def activateSNAPplugin(self, dirPath):
        self.activateThis(
                "PythonPlugins/processing_gpf",
                "Processing/configuration/ACTIVATE_SNAP")
        self.activateThis(
                "Processing/configuration/S1TBX_ACTIVATE",
                "Processing/configuration/S2TBX_ACTIVATE")
        self.setQGISSettings("Processing/configuration/SNAP_FOLDER", dirPath)

    def activateRplugin(self, dirPath, use64):
        self.activateThis(
                "Processing/configuration/ACTIVATE_R")
        self.setQGISSettings("Processing/configuration/R_FOLDER", dirPath)
        self.setQGISSettings("Processing/configuration/R_USE64", use64)

    def activateSWATplugin(self, dirPath):
        self.activateThis(
                "PythonPlugins/processing_SWAT",
                "Processing/configuration/ACTIVATE_WG9HM")
        self.setQGISSettings("Processing/configuration/MAPWINDOW_FOLDER", dirPath)


if __name__ == '__main__':

    logfile = _set_logfile_handler()

    try:
        app = QtGui.QApplication(sys.argv)

        installer = Installer(logfile=logfile)

        # Fix to make sure that runInstaller is executed in the app event loop
        def _slot_installer():
            QtCore.SLOT(installer.runInstaller())

        QtCore.QTimer.singleShot(200, _slot_installer)

        app.exec_()
    except:
        logger.exception()
        raise
