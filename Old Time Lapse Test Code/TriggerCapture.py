from time import sleep #Import all necesary libraries
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess


def killgphoto2Process ():   #Kill gphoto2 process that starts when you connect camera.
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate ()

    for line in out.splitlines ():    #Search for the line that has process we want to kill
        if b'gvfsd-gphoto2' in line:
            pid = int (line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL) #kills process

#Define variables
shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

clearCommand = ["--folder", "/store_00010001/DCIM/101D3400", "-R", "--delete-all-files"]
#imageCommand = ["--trigger-capture"]
imageCommand = ["--capture-image-and-download"]
# --wait-event-and-download
downloadCommand = ["--get-all-files"]
picID = "piShots"
saveFolder = "SaveFolderError"
numPictures = 1
delayDuration = 1
saveLocation = "/home/pi/Desktop/gphoto/images/" + saveFolder
saveLocation_time = "/home/pi/Desktop/gphoto/images/" + shot_time

#Subprograms
def getInputs(): #Gets inputs
    print("Enter the amount of photos to be taken:") #numPictures = amount of pictures to take
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

def createSaveFolder(): #Creates Save folder, uses 'saveFolder' variable to name
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
    #gp(downloadCommand)
    #gp(clearCommand)
    renameFiles(picID) #Maybe remove this and do after to optimize??

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

#Main
killgphoto2Process()
gp(clearCommand)
getInputs()
createSaveFolder()

count = 0
while (count < numPictures):
    count = count + 1
    captureImages()
    print(count)
    sleep(delayDuration)
print("Time Lapse Finished")
