
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
# the actual Interpriter
def LGOGScriptInterpriter(gameDir,winePrefix):
    #find install script
    scriptPath = os.path.join(gameDir,'goggame-*.script')
    for scriptz in glob.glob(scriptPath):
        # open script
        with open(os.path.join(gameDir,scriptz),'r') as InstallScript:
            # read script
            InstallSkrypt = InstallScript.read()
            # parse script json
            for action in json.loads(InstallSkrypt)['actions']:
                # create save paths
                if action['install']['action'] == 'supportData':
                    if action['install']["arguments"]["type"] == "folder":
                        #remove {userdocs}\\ from string
                        folder = action['install']['arguments']["target"].replace('{userdocs}/', '')
                        #find wine C:\\users\\* folders
                        OsWalkies = [throwaway1[1] for throwaway1 in os.walk(os.path.join(winePrefix,'drive_c/users'))]
                        for UserDir in OsWalkies[0]:
                            # make folder
                            os.makedirs(os.path.join(winePrefix,'drive_c/users/',UserDir ,'Documents',folder), exist_ok = True)
                    if action['install']["arguments"]["type"] == "file":
                        source = action['install']['arguments']["source"]
                        target = action['install']['arguments']["target"]
                        if '{userdocs}' in target:
                            OsWalkies = [throwaway1[1] for throwaway1 in os.walk(os.path.join(winePrefix,'drive_c/users'))]
                            for UserDir in OsWalkies[0]:
                                if not os.path.exists(os.path.join(winePrefix,'drive_c/users/',UserDir,'Documents',target)):
                                    if '{app}' in source:
                                        source = os.path.join(gameDir,source.replace('{app}/',''))
                                    shutil.copyfile(source, os.path.join(winePrefix,'drive_c/users/',UserDir,target))
                            else:
                                if not os.path.exists(target):
                                    if '{app}' in source:
                                        source = os.path.join(gameDir,source.replace('{app}/',''))
                                shutil.copyfile(source,target)
                # handel basic RegEdit Actions
                elif action['install']['action'] == "setRegistry":
                        #format subkey
                        subkey = action['install']['arguments']['subkey']
                        subkey = subkey.replace('Software\\','Software\\Wow6432Node\\').replace('\\','\\\\')
                        # get value (currently only does string)
                        valueName = action['install']['arguments']['valueName']
                        valueData = action['install']['arguments']['valueData']
                        # get install dir if data contains "{app}"
                        if '{app}' in valueData:
                            #Find Wine Path
                            valueData = EuclidsCFinder(gameDir,winePrefix).replace("\\","\\\\")
                        # format Regestry spew
                        # i know it's terible RegFile Formatting but Wine Knows what to do with it already
                        RegestryData = [
                            r'['+ subkey + ']',
                            r'"'+ valueName + '"="' + valueData + '"',
                            ]
                        # append to RegestryFile
                        with open(os.path.join(winePrefix,"system.reg"), "a") as RegestryFile:
                            for iterator in RegestryData:
                                RegestryFile.write("\n")
                                RegestryFile.write(iterator)
# basic approach to running every exe in /__redist/ : assumes wine is installed
def LGOGRedistributableInstall(gameDir,winePrefix):
    for root, dirs, files in os.walk(os.path.join(gameDir,"__redist")):
        for file in files:
            if file.upper().endswith(".EXE"):
                os.system('WINEPREFIX="'+winePrefix+'" wine "' +os.path.join(root,file)+ '"')
LGOGScriptInterpriter(sys.argv[1],sys.argv[2])
LGOGRedistributableInstall(sys.argv[1],sys.argv[2])
