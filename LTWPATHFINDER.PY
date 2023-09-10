#-----------HallinbircH Linux Path To Wine Path Scroll--------------------------
# by Lyosiss HallinbircH (Elijah Ward)
#
#
def WinePathfinderSpell(LinuxPath): # keep this because it only needs the one argument
    return "Z:" + LinuxPath.replace("/","\\")
# to define a function to return a wine-ified version of a linux path.
def EuclidsCFinder(LinuxPath,winePrefix):
    if winePrefix+"drive_c" in LinuxPath:
        return LinuxPath.replace(winePrefix+"drive_c","C:").replace("/","\\")
    else:
        return WinePathfinderSpell(LinuxPath)
# Made For A FONV install but it has other posible applications
