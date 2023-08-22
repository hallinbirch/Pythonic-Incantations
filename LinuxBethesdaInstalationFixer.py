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
import re
from LinuxToWinePath import EuclidsCFinder
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
def BethesdaSoftRegRemove(GameID, winePrefix):
    with open(os.path.join(winePrefix,"system.reg"), "r") as RegestryFile1:
         Reg = RegestryFile1.read()
         pattern = re.compile(r'\[Software\\\\Wow6432Node\\\\Bethesda Softworks\\\\'+GameID+r'.*Installed Path.*"', re.DOTALL)
         res = pattern.findall(Reg)
         Reg2 = Reg
         for stuff in res:
            Reg2 = Reg2.replace(stuff, '')
    with open(os.path.join(winePrefix,"system.reg"), "w") as RegestryFile1:
         RegestryFile1.write(Reg2)
def BethSoftRegFixGen(GameID,GamePath):
    return [
        r'[Software\\Wow6432Node\\Bethesda Softworks\\'+ GameID +']',
        r'"Installed Path"="'+ GamePath + '"',
        ]
# Skyrim SE GOG Work Around
def SkyrimSEGOGWorkaround(GamePath):
    # for some reason the game is tied into the GOG inno install Regestry Entry
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
def Fallout4GOGWorkaround(GamePath,winePrefix,gameDir):
    # OMG 5 lines to do somthing Fallout4Launcher.exe should do automatically!
        OsWalkies = [throwaway1[1] for throwaway1 in os.walk(os.path.join(winePrefix,'drive_c/users'))]
        for UserDir in OsWalkies[0]:
            os.makedirs(os.path.join(winePrefix,'drive_c/users/',UserDir ,'Documents/My Games/Fallout4/Saves'), exist_ok = True),

            if not os.path.exists(os.path.join(winePrefix,'drive_c/users/',UserDir,'Documents/My Games/Fallout4/','Fallout4.ini')):
                shutil.copyfile(os.path.join(gameDir,'Fallout4_Default.ini'), os.path.join(winePrefix,'drive_c/users/',UserDir,'Documents/My Games/Fallout4/','Fallout4.ini'))
            # then the standard reg genorator script works
            return BethSoftRegFixGen("Fallout4",GamePath)
def fixBethesdaInstall(gameDir,winePrefix):
    #Find Wine Path
    GamePath = EuclidsCFinder(gameDir,winePrefix)
    #Format for the RegestryFile
    GamePath = GamePath.replace("\\","\\\\")
    #Find the Game ID
    GameID = getBethesdaID(gameDir)
    # Gets SkyrimSE working on Heroic too
    if GameID == "SkyrimSE":
        GamePreset = SkyrimSEGOGWorkaround(GamePath)
    # i had a little Trouble with the ini file but it works now
    elif GameID == "Fallout4":
        GamePreset = Fallout4GOGWorkaround(GamePath,winePrefix,gameDir)
    # fall back to good old bethesda softworks format for MW OB and FONV
    else:
        GamePreset = BethSoftRegFixGen(GameID,GamePath)
    #open and append to RegestryFile
    print("cleaning Previus instalation from Regestry")
    BethesdaSoftRegRemove(GameID, winePrefix)
    print("installing Regestry Data")
    with open(os.path.join(winePrefix,"system.reg"), "a") as RegestryFile:
        for iterator in GamePreset:
            RegestryFile.write("\n")
            RegestryFile.write(iterator)
if sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print ( "This script appends a bethesda game's install directory to the wine system.reg to get it to work in any wine prefix\n" +
            "Currently only  Morrowind, Oblivion, Fallout 3, Fallout:NV, and GOG versions of Fallout 4, and Skyrim SE Are Supported \n " +
            "But it should work for thoes fairly well. \n"
            "usage : python LinuxBethesdaInstalationFixer.py 'Game-Install-Directory' 'Wine-Prefix-Folder-Path' \n" +
            "both arguments are positinal and required! \n")
else:
    print("casting Greater fix Bethesda Install")
    fixBethesdaInstall(sys.argv[1],sys.argv[2])
