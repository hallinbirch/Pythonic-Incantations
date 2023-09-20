
## --HalinbircH's LiTHIUM GOG Install Script Interpriter v.0.0.0.2--
##  by Lyosiss HalinbircH (Elijah Ward)
## Actually works for dragon age and a few other things right now
## it Needs More Testing and a lot more Work and is nowhere near complete
## Any BethesdaSoftworks Gog games should work now-ish
##
import json
import glob
import os
import sys
import shutil
## Move WinePathfinder and Cfinder into this script
def WinePathfinderSpell(LinuxPath): # keep this because it only needs the one argument
    return "Z:" + LinuxPath.replace("/","\\")

# to define a function to return a wine-ified version of a linux path.
def EuclidsCFinder(LinuxPath,winePrefix):
    if winePrefix+"drive_c" in LinuxPath:
        return LinuxPath.replace(winePrefix+"drive_c","C:").replace("/","\\")
    else:
        return WinePathfinderSpell(LinuxPath)

## made everything function again
## install support data
def supportDataInstaller(action,gameDir,winePrefix,productId):
    if action['install']["arguments"]["type"] == "folder":
        #remove {userdocs}\\ from string
        target = action['install']['arguments']["target"]
        #find wine C:\\users\\* folders
        OsWalkies = [throwaway1[1] for throwaway1 in os.walk(os.path.join(winePrefix,'drive_c/users'))]
        for UserDir in OsWalkies[0]:
            if '{userdocs}' in target:
                target = os.path.join(winePrefix,'drive_c/users/',UserDir ,'Documents',target.replace('{userdocs}',""))
            if '{userappdata}/../' in target:
                target = os.path.join(winePrefix,'drive_c/users/',UserDir,'AppData',target.replace('{userappdata}/../',''))
            # make folder
            os.makedirs(target, exist_ok = True)

    if action['install']["arguments"]["type"] == "file":
        source = action['install']['arguments']["source"]
        target = action['install']['arguments']["target"]
        if '{app}' in source:
            source = os.path.join(gameDir,source.replace('{app}/',''))
        if '{supportDir}' in source:
            source = source.replace('{supportDir}',os.path.join(gameDir,"support",productId))
        if '{userdocs}' in target:
            OsWalkies = [throwaway1[1] for throwaway1 in os.walk(os.path.join(winePrefix,'drive_c/users'))]
            for UserDir in OsWalkies[0]:
                if not os.path.exists(os.path.join(winePrefix,'drive_c/users/',UserDir,'Documents',target)):
                    target = os.path.join(winePrefix,'drive_c/users/',UserDir,'AppData',target.replace('{userdocs}',''))
        elif '{userappdata}/../' in target:
            OsWalkies = [throwaway1[1] for throwaway1 in os.walk(os.path.join(winePrefix,'drive_c/users'))]
            for UserDir in OsWalkies[0]:
                if not os.path.exists(os.path.join(winePrefix,'drive_c/users/',UserDir,'AppData',target)):
                    target = os.path.join(winePrefix,'drive_c/users/',UserDir,'AppData',target.replace('{userappdata}/../',''))
        shutil.copyfile(source,target)
# make regedit string list
def RegEditActionSorter(action,RegEditData,Cfound):
    #format subkey
    subkey = action['install']['arguments']['subkey']
    subkey = subkey.replace('Software\\','Software\\Wow6432Node\\').replace('\\','\\\\')
    subkey = '['+ subkey + ']'
    # get value (currently only does string)
    valueName = action['install']['arguments']['valueName']
    valueData = action['install']['arguments']['valueData']
    # get install dir if data contains "{app}"
    if '{app}' in valueData:
        #Find Wine Path
        valueData = Cfound.replace("\\","\\\\")
    if not subkey in RegEditData:
        RegEditData.append(subkey)
    # good old slice 'n slpice
    RegEditData = RegEditData[RegEditData.index(subkey):] + ['"'+ valueName + '"="' + valueData + '"'] + RegEditData[:RegEditData.index(subkey)]
    return RegEditData
# acually write to reg file
def AppendtoRegFile(winePrefix,RegEditData):
        with open(os.path.join(winePrefix,"system.reg"), "a") as RegestryFile:
            for iterator in RegEditData:
                RegestryFile.write("\n")
                RegestryFile.write(iterator)
#run Support EXE : it kinda assumes its in support folder
def RunSupportEXE(action,gameDir,winePrefix,productId):
    EXE = action['install']['arguments']["executable"]
    print ("Executing Exe:")
    print ("wine "+os.path.join(gameDir,"support",productId,EXE))
    os.system("wine "+os.path.join(gameDir,"support",productId,EXE))
# install all redist EXE files : I still need to fix this
def LGOGRedistributableInstall(gameDir,winePrefix):
    for root, dirs, files in os.walk(os.path.join(gameDir,"__redist")):
        for file in files:
            if file.upper().endswith(".EXE"):
                os.system('WINEPREFIX="'+winePrefix+'" wine "' +os.path.join(root,file)+ '"')
#### begin Terible Fixes for Weird EdgeCases
def TFFWECSkyrimSEGOG(GamePath):
    return [
    r'[Software\\Wow6432Node\\GOG.com\\Games\\1711230643] ',
    r'"exe"="'+ GamePath + '\\\\SkyrimSELauncher.exe"',
    r'"exeFile"="SkyrimSELauncher.exe"',
    r'"gameID"="1711230643"',
    r'"gameName"="The Elder Scrolls V: Skyrim Special Edition"',
    r'"lang_code"="en-US"',
    r'"language"="english"',
    r'"path"="'+ GamePath + '"'
    ]
def TeribleFixesforWeirdEdgeCases(gameDir,winePrefix):
    if os.path.exists(os.path.join(gameDir,"SkyrimSE.exe")):
        GamePath = EuclidsCFinder(gameDir,winePrefix)
        GamePath = GamePath.replace("\\","\\\\")
        print("SkyrimSE Found Aplaying Terible Fix For Weird Edge Case")
        RegEditData = TFFWECSkyrimSEGOG(GamePath)
        AppendtoRegFile(winePrefix,RegEditData)
        return True
    else:
        return False
#### End Terible Fixes for Weird EdgeCases
# basic "main" function with a diffrent name
def LGOGScriptInterpriter(gameDir,winePrefix):
    Cfound = EuclidsCFinder(gameDir,winePrefix)
    #find install script
    RegEditData = []
    Regeditbool = False
    WHPrun = TeribleFixesforWeirdEdgeCases(gameDir,winePrefix)
    if not WHPrun:
        scriptPath = os.path.join(gameDir,'goggame-*.script')
        for scriptz in glob.glob(scriptPath):
            # open script
            with open(os.path.join(gameDir,scriptz),'r') as InstallScript:
                # read script
                InstallSkrypt = InstallScript.read()
                # parse script json
                script = json.loads(InstallSkrypt)
                productId = script["productId"]
                for action in script['actions']:
                    if action['install']['action'] == 'supportData':
                        supportDataInstaller(action,gameDir,winePrefix,productId)
                    elif action['install']['action'] == "Execute":
                        RunSupportEXE(action,gameDir,winePrefix)
                    elif action['install']['action'] == "setRegistry":
                        if 'valueName' in action['install']['arguments']:
                            RegEditData = RegEditActionSorter(action,RegEditData,Cfound)
                            Regeditbool = True
                if Regeditbool:
                    AppendtoRegFile(winePrefix,RegEditData)
LGOGScriptInterpriter(sys.argv[1],sys.argv[2])
