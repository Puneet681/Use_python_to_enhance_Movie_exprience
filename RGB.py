import os
import cv2
import numpy as np
import pyautogui
import PIL
import PIL.ImageGrab as ImageGrab
import imutils
import time
import psutil
from zipfile import ZipFile

box = (760,100,1160,980) #Android screen coordinates

try:
	# Create a ZipFile Object and load sample.zip in it
	with ZipFile('scrcpy-win64.zip', 'r') as zipObj:
		# Extract all the contents of zip file in current directory
		zipObj.extractall()
		print('>> "scrcpy-win64" Extraction complete')
except Exception as e:
	pass

def checkIfProcessRunning(processName):
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def convert_time(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


#Excluding from running two mirrors of android screen
if checkIfProcessRunning('scrcpy-noconsole.exe'):
	print('>> Android screen already mirrored')
else:
	print('>> Mirroring android screen')
	os.system('start scrcpy-win64/scrcpy-noconsole.exe')

#initializing program
run_status = 1
st = time.time()

#Reading paths
orig_dir = os.getcwd()
adb_dir = os.path.join(os.getcwd(), "scrcpy-win64")

# input('>> Press Enter to continue')

while True:
	#Reading frames from screen
	screen = ImageGrab.grab(box)
	screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
	screen = imutils.resize(screen, height=600)

	#reading time elapsed
	et = time.time()
	elapsed_time = et-st
	elapsed_time = round(elapsed_time)

	cv2.imshow('Screen', screen)

	screen.shape
	w = (screen.shape)[0]
	h = (screen.shape)[1]
	print(screen.shape)
	rgb_list= []
	for i in range (0,h-1):
		B,G,R=screen[0,i]
		rgb_list.append((B,G,R))
	for i in range (0,w-1):
		B,G,R=screen[i,h-1]
		rgb_list.append((B,G,R))
	for i in range (h-1,0,-1):
		B,G,R=screen[w-1,i]
		rgb_list.append((B,G,R))
	for i in range (w-1,0,-1):
		B,G,R=screen[i,0]
		rgb_list.append((B,G,R))

	for i in rgb_list:
		print(i)
	len(rgb_list)

	run_status +=1
	key = cv2.waitKey(1)
	if key == ord("q"):
		cv2.destroyAllWindows()
		break