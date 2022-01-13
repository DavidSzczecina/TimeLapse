from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess


#gconftool --type Boolean --set /apps/nautilus/preferences/media_automount false!!!!!!!!!



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
picID = "PiShots"

clearCommand = ["--folder", "/store_00010001/DCIM/101D3400", "-R", "--delete-all-files"]

triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

folder_name = shot_date + picID
save_location = "/home/pi/Desktop/gphoto/images/" + folder_name


def createSaveFolder():
    try:
        os.makedirs(save_location)

    except:
        print("Failed to create the new directory.")
    os.chdir(save_location)

def captureImages():
    gp(triggerCommand)
    sleep(3)
    gp(downloadCommand)
    gp(clearCommand)


def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                os.rename(filename, (shot_time + ID + ".JPG"))
                print("Renamed the JPG")
            elif filename.endswith(".NEF"):
                os.rename(filename, (shot_time + ID + ".NEF"))
                print("Renamed the NEF")

killgphoto2Process()
gp(clearCommand)
createSaveFolder()
captureImages()
renameFiles(picID)
