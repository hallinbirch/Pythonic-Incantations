# now This is a Wierd one Made Speciffically To stitch files from Dumped Ps3 Games
import os
import sys
fileList = []
for file in sys.argv[1:-2]:
    fileList.append(file)
with open(sys.argv[-1], 'wb') as StitchedFile:
    for inputFile in fileList:
        with open(inputFile, 'rb') as InputStream:
            StitchedFile.write(InputStream.read())
