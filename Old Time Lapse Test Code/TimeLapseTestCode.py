#Camera on
#Disable USB drivers
#
#Take photo
#Transfer to PI
#Wait x amount of time
#Repeat 3-5
#
#Camera Off

from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess


#Kill gphoto2 process that starts when you connect camera.
def killgphoto2Process ():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate ()

    #Search for the line that has process we want to kill
    for line in out.splitlines ():
        if b'gvfsd-gphoto2' in line:
            #kills process
            pid = int (line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)
            

shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

clearCommand = ["--folder", "/store_00010001/DCIM/101D3400", "-R", "--delete-all-files"]
#imageCommand = ["--trigger-capture"]
imageCommand = ["--capture-image"]
downloadCommand = ["--get-all-files"]
picID = "piShots"
saveFolder = "SaveFolderError"
numPictures = 1
delayDuration = 1 


saveLocation = "/home/pi/Desktop/gphoto/images/" + saveFolder
saveLocation_time = "/home/pi/Desktop/gphoto/images/" + shot_time

def getInputs():
    print("Enter the amount of photos to be taken:") #numPictures = amount of pictures to tale
    numPicturesStr = input()
    global numPictures
    numPictures = int(numPicturesStr)

    print("Enter the delay between each photo:") #delayDuration = seconds between each photo
    delayDurationStr = input()
    global delayDuration
    delayDuration = int(delayDurationStr)

    print("Enter save folder name:") #saveFolder = name of save folder where photos go
    global saveFolder
    saveFolder = input()
    saveLocation = "/home/pi/Desktop/gphoto/images/" + saveFolder

def createSaveFolder():
    try:
        saveLocation = "/home/pi/Desktop/gphoto/images/" + saveFolder
        os.makedirs(saveLocation)
        os.chdir(saveLocation)
    except:
        print("Failed to create the new directory, Saved as Date/Time")
        saveLocation_time = "/home/pi/Desktop/gphoto/images/" + shot_time
        os.makedirs(saveLocation_time)
        os.chdir(saveLocation_time)

def captureImages():
    gp(imageCommand)
    gp(downloadCommand)
    gp(clearCommand)


def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                os.rename(filename, (shot_time + ".JPG"))
                print("Renamed the JPG")
            elif filename.endswith(".NEF"):
                os.rename(filename, (shot_time + ".NEF"))
                print("Renamed the NEF")




killgphoto2Process()
gp(clearCommand)
getInputs()
createSaveFolder()

count = 0
while (count < numPictures):   
    count = count + 1

  #  gp(clearCommand)

    #createSaveFolder()
    captureImages()
    renameFiles(picID)

    sleep(delayDuration)
print("Time Lapse Finished")
