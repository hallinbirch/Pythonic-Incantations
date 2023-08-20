# -----HalinbircH's Greater Fix Bethesda Install for Wine Scroll---------
#    by Lyosiss HalinbircH (Elijah Ward)
#    License : GNU GPL3
#   Requires : HalinbircH's LinuxToWinePath Scroll and several Default Python Libs
#   Helps With Skyrim SE GOG on Heroic for Linux!
#
# import Dependecies
import os
import sys
import platform
import shutil
from LinuxToWinePath import EuclidsCFinder
import random
#find out what game we're looking at
def getBethesdaID(gameDir):
    # Older Bethesda Games Work Really Well
    if os.path.exists(os.path.join(gameDir,"Morrowind.exe")):
        return "Morrowind"
    elif os.path.exists(os.path.join(gameDir,"Oblivion.exe")):
        return "Oblivion"
    elif os.path.exists(os.path.join(gameDir,"Fallout3.exe")):
        return "Fallout3"
    elif os.path.exists(os.path.join(gameDir,"FalloutNV.exe")):
        return "FalloutNV"
    # start of games requiring hackey work arounds
    elif os.path.exists(os.path.join(gameDir,"SkyrimSE.exe")):
        return "SkyrimSE"
    elif os.path.exists(os.path.join(gameDir,"Fallout4.exe")):
        return "Fallout4"
def BethSoftRegFixGen(GameID,GamePath,randomNumber):
    return [
        r'[Software\\Wow6432Node\\Bethesda Softworks\\'+ GameID +'] ' + str(randomNumber),
        r'#time=1d9ceebed86feec',
        r'"Installed Path"="'+ GamePath + '"',
        ]
# Skyrim SE GOG Work Around
def SkyrimSEGOGWorkaround(GamePath,randomNumber):
    # for some reason the game is tied into the GOG inno genorated install Regestry Entry
    return [
    r'[Software\\Wow6432Node\\GOG.com\\Games\\1711230643] ' + str(randomNumber),
    r'#time=1d9cac8fe679c02',
    r'"buildId"="55846306920288567"',
    r'"dependsOn"=""',
    r'"DLC"="1162721350"',
    r'"exe"="'+ GamePath + 'SkyrimSELauncher.exe"',
    r'"exeFile"="SkyrimSELauncher.exe"',
    r'"gameID"="1711230643"',
    r'"gameName"="The Elder Scrolls V: Skyrim Special Edition"',
    r'"INSTALLDATE"="2023-08-09 00:31:48"',
    r'"installer_language"="english"',
    r'"lang_code"="en-US"',
    r'"language"="english"',
    r'"launchCommand"="'+GamePath+'SkyrimSELauncher.exe "',
    r'"launchParam"=""',
    r'"osbit"="64"',
    r'"path"="'+ GamePath + '"',
    r'"productID"="1711230643"',
    r'"startMenu"="The Elder Scrolls V - Skyrim Special Edition"',
    r'"startMenuLink"="C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\The Elder Scrolls V - Skyrim Special Edition [GOG.com]\\The Elder Scrolls V - Skyrim Special Edition"',
    r'"supportLink"=""',
    r'"uninstallCommand"="' + GamePath + 'unins000.exe"',
    r'"ver"="1.6.659.0.8"',
    r'"workingDir"="' + GamePath + '"'
    ]
def Fallout4GOGWorkaround(GamePath,randomNumber,winePrefix,gameDir):
    # OMG 5 lines to do somthing Fallout4Launcher.exe should do automatically!
        OsWalkies = [throwaway1[1] for throwaway1 in os.walk(os.path.join(winePrefix,'drive_c/users'))]
        for UserDir in OsWalkies[0]:
            os.makedirs(os.path.join(winePrefix,'drive_c/users/',UserDir ,'Documents/My Games/Fallout4/Saves'), exist_ok = True),

            if not os.path.exists(os.path.join(winePrefix,'drive_c/users/',UserDir,'Documents/My Games/Fallout4/','Fallout4.ini')):
                shutil.copyfile(os.path.join(gameDir,'Fallout4_Default.ini'), os.path.join(winePrefix,'drive_c/users/',UserDir,'Documents/My Games/Fallout4/','Fallout4.ini'))
            # then the standard reg genorator script works
            return BethSoftRegFixGen("Fallout4.exe",GamePath,randomNumber)
def fixBethesdaInstall(gameDir,winePrefix):
    random.seed(a=None, version=2)
    #Find Wine Path
    GamePath = EuclidsCFinder(gameDir,winePrefix)
    #Format for the RegestryFile
    GamePath = GamePath.replace("\\","\\\\")
    #Find the Game ID
    GameID = getBethesdaID(gameDir)
    #Format the whole thing
    randomNumber = random.randrange(1692999999,9999999999)
    # Gets SkyrimSE working on Heroic too
    if GameID == "SkyrimSE":
        GamePreset = SkyrimSEGOGWorkaround(GamePath,randomNumber)
    # i had a little Trouble with the ini file but it works now
    elif GameID == "Fallout4":
        GamePreset = Fallout4GOGWorkaround(GamePath,randomNumber,winePrefix,gameDir)
    # fall back to good old bethesda softworks format for MW OB and FONV
    else:
        GamePreset = BethSoftRegFixGen(GameID,GamePath,randomNumber)
    #open and append to RegestryFile
    with open(os.path.join(winePrefix,"system.reg"), "a") as RegestryFile:
        for iterator in GamePreset:
            RegestryFile.write("\n")
            RegestryFile.write(iterator)
print("casting Greater fix Bethesda Install")
if sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print ( "This script appends a bethesda game's install directory to the wine system.reg to get it to work in any wine prefix\n" +
            "Currently only  Morrowind, Oblivion, Fallout 3, Fallout:NV, and GOG versions of Fallout 4, and Skyrim SE Are Supported \n " +
            "But it should work for thoes fairly well. \n"
            "usage : python LinuxBethesdaInstalationFixer.py 'Game-Install-Directory' 'Wine-Prefix-Folder-Path' \n" +
            "both arguments are positinal and required! \n")
else:
    fixBethesdaInstall(sys.argv[1],sys.argv[2])
