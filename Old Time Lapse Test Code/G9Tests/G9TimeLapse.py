# David Szczecina
# 16/21/2021
#Time Lapse Script for g9


#gphoto2 --set-config beep=0 --set-config flashmode=0 --set-config resolution=3 -I 20 -F 3150 --capture-image-and-download --filename "%03n%Y%m%d%H%M%S.jpg"

#Breakdown
#--set-config beep=0, No beep
#--set-config flashmode=0, No flash
#--set-config resolution=3, check max resolution
#-I     seconds between photos
#-F     amount of photos
#--filename "%03n%Y%m%d%H%M%S.jpg"      Filename: 001/Y/M/D/H/M/S.jpg


from time import sleep #Import all necesary libraries
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

#edit 1

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

# TODO: default store folder name
clearCommand = ["--folder", "/store_00010001/DCIM/100PICS_", "-R", "--delete-all-files"]
downloadCommand = ["--get-all-files"]

saveFolder = "SaveFolderError"
numPictures = "1"
delayDuration = "1"

saveLocation = "/home/pi/Desktop/gphoto/images/" + saveFolder
saveLocation_time = "/home/pi/Desktop/gphoto/images/" + shot_time

#imageCommand = ["gphoto2 --set-config beep=0 --set-config flashmode=0 --set-config resolution=3 -I "delayDuration" -F "numPictures" --capture-image-and-download --filename "%03n%Y%m%d%H%M%S.jpg""]
imageCommandStr = "gphoto2 -I "+ delayDuration +" -F "+ numPictures +" --capture-image-and-download --filename %03n%Y%m%d%H%M%S.jpg"



#Subprograms
def getInputs(): #Gets inputs
    print("Enter the amount of photos to be taken:") #numPictures = amount of pictures to take
    global numPictures
    numPictures = input()

    print("Enter the delay between each photo:") #delayDuration = seconds between each photo
    global delayDuration
    delayDuration = input()

    print("Enter save folder name:") #saveFolder = name of save folder where photos go
    global saveFolder
    saveFolder = input()
    saveLocation = "/home/pi/Desktop/gphoto/images/" + saveFolder

    global imageCommandStr  #Update imageCommand
    imageCommandStr = "gphoto2 -I "+ delayDuration +" -F "+ numPictures +" --capture-image-and-download --filename %03n%Y%m%d%H%M%S.jpg"


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
    os.system(imageCommandStr)



#Main
killgphoto2Process()
gp(clearCommand)
getInputs()
createSaveFolder()
print(imageCommandStr)
captureImages()
print("Time Lapse Finished")
