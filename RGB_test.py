# currenty working
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
from PIL import Image
import time
# import board
# import neopixel


box = (196,146,1720,960)  #Android screen coordinates

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
# setting GPIO pin
# pixels1 = neopixel.NeoPixel(board.D18, 55, brightness=1)

while True:
	#Reading frames from screen
	screen = ImageGrab.grab(box)
	screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
	screen = imutils.resize(screen, height=600)

	#reading time elapsed
	et = time.time()
	elapsed_time = et-st
	elapsed_time = round(elapsed_time)

	screen.shape
	w = (screen.shape)[0]
	h = (screen.shape)[1]
	print(screen.shape)

	time.sleep(3)

	loc_RGB= []
	for i in range (0,h-1):
		x = 0
		y = i
		B,G,R=screen[0,i]
		loc_RGB.append([(x,y),(R,G,B)])
	for i in range (0,w-1):
		x = i
		y = h-1
		B,G,R=screen[i,h-1]
		loc_RGB.append([(x,y),(R,G,B)])
	for i in range (h-1,0,-1):
		x = w-1
		y = i
		B,G,R=screen[w-1,i]
		loc_RGB.append([(x,y),(R,G,B)])
	for i in range (w-1,0,-1):
		x = i
		y = 0
		B,G,R=screen[i,0]
		loc_RGB.append([(x,y),(R,G,B)])


#  to test the if the RGB values nad there location is correct or not
	size = (int(w),int(h))
	img = Image.new('RGB',size)

	data = img.load()
	for i in loc_RGB:
			# print(i)
			x = i[0][0]
			y = i[0][1]
			R = i[1][0]
			G = i[1][1]
			B = i[1][2]
			data[x,y] = (R,G,B)

			# pixels1[i]=(R,G,B)

	img.show()
	break
	# time.sleep(1.5)