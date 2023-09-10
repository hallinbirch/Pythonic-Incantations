import csv
import requests
import os
import time
outputDir = "/home/halinbirch/test/"
with open('CardImageLinks.csv', newline='') as csvfile:
    cardscsv = csv.DictReader(csvfile, delimiter=';', quotechar='|')
    for card in cardscsv:
        print ("Loading Card From Set: " + card["id"] + " With Id of: " + card["set"])
        ImagePath = os.path.join(outputDir,card["id"],card["set"]+".jpg")
        os.makedirs(os.path.join(outputDir,card["id"]), exist_ok = True)
        if os.path.exists(ImagePath):
            print('"'+ImagePath+'" Exists Already: Skiping!')
        else:
            with open(ImagePath, 'wb') as Image:
                while True:
                    try:
                        download = requests.get(card["link		  "]).content
                    except:
                        print("Download Failed Retrying")
                    else:
                        break
                Image.write(download)
                time.sleep(2.5)
