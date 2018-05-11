# Class provides information about which platform code is running on
#
# Created:
# May 11: Marcus Saikaley

import sys

class PlatformInfo:
    platformID  = []    # 1 - macosx, 2 - windows, 3 - linux
    pythonVer   = []

    # get platform id
    def getPlatformID(self):
        if sys.platform == "darwin":
            return 1
        elif sys.platform == "win32":
            return 2

    # get python version in current environment
    def getPythonVersion(self):
        return sys.version_info[:2]

    # default constructor
    def __init__(self):
        self.platformID = self.getPlatformID()
        self.pythonVer  = self.getPythonVersion()

    # is this running on a mac
    def isMac(self):
        return self.platformID == 1

    # is this running on windows
    def isWindows(self):
        return self.platformID == 2

    # print python version in active environment
    def printPythonVer(self):
        print("Current python version is " + str(self.pythonVer))
