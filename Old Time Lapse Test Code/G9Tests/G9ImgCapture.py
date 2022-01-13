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
#downloadCommand = ["--get-all-files"]
picID = "piShots"
saveLocation = "/home/pi/Desktop/gphoto/images/" + shot_time

def createSaveFolder():
        saveLocation = "/home/pi/Desktop/gphoto/images/" + shot_time
        os.makedirs(saveLocation)
        os.chdir(saveLocation)

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
#gp(clearCommand)
createSaveFolder()
captureImages()
print("Done")
