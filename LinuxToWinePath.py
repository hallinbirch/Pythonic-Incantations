#-----------HallinbircH Linux Path To Wine Path Scroll--------------------------
# by Lyosiss HallinbircH (Elijah Ward)
#
#
def WinePathfinderSpell(LinuxPath): # keep this because it only needs the one argument
    return "Z:" + LinuxPath.replace("/","\\")
# to define a function to return a wine-ified version of a linux path.
def EuclidsCFinder(LinuxPath,winePrefix):
    print("EuclidsCFinder : Finding 'C:'")
    if winePrefix+"drive_c" in LinuxPath:
        print("'EuclidsCFinder: C: Found")
        return LinuxPath.replace(winePrefix+"drive_c","C:").replace("/","\\")
    else:
        print("EuclidsCFinder: C: Not Found")
        print("EuclidsCFinder: Z: Found")
        return WinePathfinderSpell(LinuxPath)
# to do it all in the clipboard
