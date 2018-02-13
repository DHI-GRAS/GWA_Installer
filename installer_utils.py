import os
import re
import sys
import shutil
import tempfile
import ctypes
import ctypes.wintypes

from PyQt4 import QtGui


def _get_ram():
    """Get amount of physical memory"""
    kernel32 = ctypes.windll.kernel32
    c_ulonglong = ctypes.c_ulonglong

    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ('dwLength', ctypes.wintypes.DWORD),
            ('dwMemoryLoad', ctypes.wintypes.DWORD),
            ('ullTotalPhys', c_ulonglong),
            ('ullAvailPhys', c_ulonglong),
            ('ullTotalPageFile', c_ulonglong),
            ('ullAvailPageFile', c_ulonglong),
            ('ullTotalVirtual', c_ulonglong),
            ('ullAvailVirtual', c_ulonglong),
            ('ullExtendedVirtual', c_ulonglong),
        ]

    memoryStatus = MEMORYSTATUSEX()
    memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))
    return (memoryStatus.ullTotalPhys)


def modifyRamInBatFiles(batFilePath, useRamFraction):
    # Check how much RAM the system has. Only works in Windows
    if sys.platform != 'win32':
        msgBox = QtGui.QMessageBox()
        msgBox.setText(
            "This installer is only meant for Windows!\n\n "
            "The installed GWA Toolbox might not work properly.")
        msgBox.exec_()
        return
    totalRam = _get_ram()
    totalRam = totalRam / (1024*1024)

    # Make sure the BEAM/SNAP batch file exists in the given directory
    if not os.path.isfile(batFilePath):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(
            "Could not find the batch file!\n\n "
            "The amount of RAM available to the program was not changed.")
        msgBox.exec_()
        return

    if batFilePath.endswith('.bat'):
        # Beam
        # In the batch file replace the amount of RAM to be used
        # by BEAM to some % of system RAM, first in a temp file
        # and then copy the temp file to the correct dir
        ram_flag = "-Xmx"+str(int(totalRam*useRamFraction))+"M"
        backupfile = batFilePath + '.backup'
        try:
            os.remove(backupfile)
        except OSError:
            pass
        shutil.move(batFilePath, backupfile)
        try:
            with open(backupfile, 'r') as infile, open(batFilePath, 'w') as outfile:
                for line in infile:
                    line = re.sub(r"-Xmx\d+[Mm]", ram_flag, line)
                    outfile.write(line)
        except:
            shutil.move(backupfile, batFilePath)
            raise

    elif batFilePath.endswith('.vmoptions'):
        # Snap
        # In the vmoptions file replace the amount of RAM to be used
        # by SNAP to some % of system RAM, first in a temp file
        # and then copy the temp file to the correct dir
        ram_flag = "-Xmx"+str(int(totalRam*useRamFraction))+"m"
        backupfile = batFilePath + '.backup'
        try:
            os.remove(backupfile)
        except OSError:
            pass
        shutil.move(batFilePath, backupfile)
        try:
            with open(backupfile, 'r') as infile, open(batFilePath, 'w') as outfile:
                for line in infile:
                    if '-Xmx' in line:
                        # omit old -Xmx flags
                        continue
                    outfile.write(line)
                outfile.write(ram_flag)
        except:
            shutil.move(backupfile, batFilePath)
            raise


def removeIncompatibleJavaOptions(self, batFilePath):
    # Make sure the snap batch file exists in the given directory
    if not os.path.isfile(batFilePath):
        raise IOError('batch file does not exist: {}'.format(batFilePath))

    # In the batch file remove the "-XX:+UseLoopPredicate"
    # option which doesn't work with 32 bit installation.
    # First do this in a temp file and then copy the temp file to the correct dir
    tempFile = tempfile.NamedTemporaryFile(delete=False)
    tempFilePath = tempFile.name
    tempFile.close()
    with open(tempFilePath, 'w') as outfile, open(batFilePath, 'r') as infile:
        for line in infile:
            line = re.sub(r"-XX:\+UseLoopPredicate ", "", line)
            outfile.write(line)
    tempDir = os.path.dirname(tempFilePath)
    tempgpt = os.path.join(tempDir, "gpt.bat")
    if os.path.isfile(tempgpt):
        os.remove(tempgpt)
    os.rename(tempFilePath, tempgpt)
    shutil.copy(tempgpt, batFilePath)


def fix_jpyconfig(path, replace):
    if not os.path.isfile(path):
        return
    path_backup = path + '.backup'
    shutil.move(path, path_backup)
    try:
        with open(path, 'w') as fout, open(path_backup, 'r') as fin:
            for line in fin:
                for key, value in replace.items():
                    if key in line:
                        line = re.sub('\=.*', '= {}'.format(value), line.rstrip()) + '\n'
                        break
                fout.write(line)
    except:
        shutil.move(path_backup, path)


def check_file_exists(filepath):
    if not os.path.isfile(filepath):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(
            "Could not find the required file \'{}\'.\n\n "
            "Skipping this step.".format(filepath))
        msgBox.exec_()
        return False
    else:
        return True
