
## --HalinbircH's Linux GOG Install Script Interpriter v.0.0.0.1--
##  by Lyosiss HalinbircH (Elijah Ward)
## All i know is it installs the witcher 2
## it Needs More Testing and a lot more Work
## TODO: add Better Redistributable installer
##
import json
import glob
import os
import sys
import shutil
from LinuxToWinePath import EuclidsCFinder
def LGOGScriptInterpriter(gameDir,winePrefix):
    scriptPath = os.path.join(gameDir,'goggame-*.script')
    for scriptz in glob.glob(scriptPath):
        with open(os.path.join(gameDir,scriptz),'r') as InstallScript:
            InstallSkrypt = InstallScript.read()
            for action in json.loads(InstallSkrypt)['actions']:
                if action['install']['action'] == 'savePath':
                    savepath = action['install']['arguments']['savePath'].replace('{userdocs}\\', '')
                    OsWalkies = [throwaway1[1] for throwaway1 in os.walk(os.path.join(winePrefix,'drive_c/users'))]
                    for UserDir in OsWalkies[0]:
                        os.makedirs(os.path.join(winePrefix,'drive_c/users/',UserDir ,'Documents',savepath), exist_ok = True),
                if action['install']['action'] == "setRegistry":
                        subkey = action['install']['arguments']['subkey']
                        subkey = subkey.replace('Software\\','Software\\Wow6432Node\\').replace('\\','\\\\')
                        valueName = action['install']['arguments']['valueName']
                        valueData = action['install']['arguments']['valueData']
                        if '{app}' in valueData:
                            #Find Wine Path
                            valueData = EuclidsCFinder(gameDir,winePrefix).replace("\\","\\\\")
                            #Format for the RegestryFile
                        RegestryData = [
                            r'['+ subkey + ']',
                            r'"'+ valueName + '"="' + valueData + '"',
                            ]
                        with open(os.path.join(winePrefix,"system.reg"), "a") as RegestryFile:
                            for iterator in RegestryData:
                                RegestryFile.write("\n")
                                RegestryFile.write(iterator)
def LGOGRedistributableInstall(gameDir,winePrefix):
    for root, dirs, files in os.walk(os.path.join(gameDir,"__redist")):
        for file in files:
            if file.upper().endswith(".EXE"):
                os.system('WINEPREFIX="'+winePrefix+'" wine "' +os.path.join(root,file)+ '"')
LGOGScriptInterpriter(sys.argv[1],sys.argv[2])
GOGRedistributableInstall(sys.argv[1],sys.argv[2])
