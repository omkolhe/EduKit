# All packages needed for the program are imported ahead
import cv2
import numpy as np
import serial

# Some global variables or others that need prior intialization are initalized here

# colour ranges for feeding to the inRange funtions 
blue_range = np.array([[88,78,20],[128,255,255]])
yellow_range = np.array([[21,70,80],[61,255,255]])
red_range = np.array([[158,85,72],[180 ,255,255]])

# Prior initialization of all centers for safety
b_cen, y_pos, r_cen = [240,320],[240,320],[240,320]
cursor = [960,540]

# Area ranges for contours of different colours to be detected
r_area = [100,1700]
b_area = [100,1700]
y_area = [100,1700]

# Rectangular kernal for eroding and dilating the mask for primary noise removal 
kernel = np.ones((7,7),np.uint8)

# Status variables defined globally
perform = False
showCentroid = False

# 'nothing' function is useful when creating trackbars
# It is passed as last arguement in the cv2.createTrackbar() function
def nothing(x):
	pass

# To bring to the top the contours with largest area in the specified range
# Used in drawContour()
def swap( array, i, j):
	temp = array[i]
	array[i] = array[j]
	array[j] = temp

# Distance between two centroids
def distance( c1, c2):
	distance = pow( pow(c1[0]-c2[0],2) + pow(c1[1]-c2[1],2) , 0.5)
	return distance

# To toggle status of control variables
def changeStatus(key):
	global perform
	global showCentroid
	global yellow_range,red_range,blue_range
	# toggle mouse simulation
	if key == ord('p'):
		perform = not perform
		if perform:
			print 'Bot simulation ON...'
		else:
			print 'Bot simulation OFF...'
	
	# toggle display of centroids
	elif key == ord('c'):
		showCentroid = not showCentroid
		if showCentroid:
			print 'Showing Centroids...'
		else:
			print 'Not Showing Centroids...'

	elif key == ord('r'):
		print '**********************************************************************'
		print '	You have entered recalibration mode.'
		print ' Use the trackbars to calibrate and press SPACE when done.'
		print '	Press D to use the default settings'
		print '**********************************************************************'

		yellow_range = calibrateColor('Yellow', yellow_range)
		red_range = calibrateColor('Red', red_range)
		blue_range = calibrateColor('Blue', blue_range)			
	
	else:
		pass

# cv2.inRange function is used to filter out a particular color from the frame
# The result then undergoes morphosis i.e. erosion and dilation
# Resultant frame is returned as mask 
def makeMask(hsv_frame, color_Range):
	
	mask = cv2.inRange( hsv_frame, color_Range[0], color_Range[1])
	# Morphosis next ...
	eroded = cv2.erode( mask, kernel, iterations=1)
	dilated = cv2.dilate( eroded, kernel, iterations=1)
	
	return dilated

# Contours on the mask are detected.. Only those lying in the previously set area 
# range are filtered out and the centroid of the largest of these is drawn and returned 
def drawCentroid(vid, color_area, mask, showCentroid):
	
	_, contour, _ = cv2.findContours( mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	l=len(contour)
	area = np.zeros(l)

	# filtering contours on the basis of area rane specified globally 
	for i in range(l):
		if cv2.contourArea(contour[i])>color_area[0] and cv2.contourArea(contour[i])<color_area[1]:
			area[i] = cv2.contourArea(contour[i])
		else:
			area[i] = 0
	
	a = sorted( area, reverse=True)	

	# bringing contours with largest valid area to the top
	for i in range(l):
		for j in range(1):
			if area[i] == a[j]:
				swap( contour, i, j)

	if l > 0 :		
		# finding centroid using method of 'moments'
		M = cv2.moments(contour[0])
		if M['m00'] != 0:
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			center = (cx,cy)
			if showCentroid:
				cv2.circle( vid, center, 5, (0,0,255), -1)
					
			return center
	else:
		# return error handling values
		return (-1,-1)

# This function helps in filtering the required colored objects from the background
def calibrateColor(color, def_range):
	
	global kernel
	name = 'Calibrate '+ color
	cv2.namedWindow(name)
	cv2.createTrackbar('Hue', name, def_range[0][0]+20, 180, nothing)
	cv2.createTrackbar('Sat', name, def_range[0][1]   , 255, nothing)
	cv2.createTrackbar('Val', name, def_range[0][2]   , 255, nothing)
	while(1):
		ret , frameinv = cap.read()
		frame=cv2.flip(frameinv ,1)

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		hue = cv2.getTrackbarPos('Hue', name)
		sat = cv2.getTrackbarPos('Sat', name)
		val = cv2.getTrackbarPos('Val', name)

		lower = np.array([hue-20,sat,val])
		upper = np.array([hue+20,255,255])

		mask = cv2.inRange(hsv, lower, upper)
		eroded = cv2.erode( mask, kernel, iterations=1)
		dilated = cv2.dilate( eroded, kernel, iterations=1)

		cv2.imshow(name, dilated)		

		k = cv2.waitKey(5) & 0xFF
		if k == ord(' '):
			cv2.destroyWindow(name)
			return np.array([[hue-20,sat,val],[hue+20,255,255]])
		elif k == ord('d'):
			cv2.destroyWindow(name)
			return def_range

'''
This function takes as input the center of yellow region (yc) and 
the previous cursor position (pyp). The new cursor position is calculated 
in such a way that the mean deviation for desired steady state is reduced.
'''

# Depending upon the relative positions of the three centroids, this function chooses whether 
# the user desires free movement of cursor, left click, right click or dragging
def chooseAction(yc, rc, bc):
	out = np.array(['stop', 'false'])
	if rc[0]!=-1 and bc[0]!=-1:
		
		if distance(rc,bc)<40: 
			out[0] = 'right'
			return out
		elif distance(yc,rc)<40:	
			out[0] = 'left'
			return out
		elif distance(yc,rc)>40 and rc[1]-bc[1]>120:
			out[0] = 'rev'
			return out	
		elif bc[1]-rc[1]>110:
			out[0] = 'for'
			return out
		else:
			return out

	else:
		out[0] = -1
		return out 		

# Movement of cursor on screen, left click, right click,scroll up, scroll down
# and dragging actions are performed here based on value stored in 'action'.  
def performAction( yc, rc, bc, action, drag, perform):
	if perform:
	 	cursor[0] = 4*(yc[0]-110)
		cursor[1] = 4*(yc[1]-120)
		
		if action == 'stop':
			print 'Stop'
			ser.write('B')

		elif action == 'left':
			print 'Left'
			ser.write('A')

		elif action == 'right':
			print 'Right'
			ser.write('D')
		
		elif action == 'for':
			print 'Forward'
			ser.write('W')

		elif action == 'rev':
			print 'Reverse'
			ser.write('S')

cap = cv2.VideoCapture(0)

print '**********************************************************************'
print '	You have entered calibration mode.'
print ' Use the trackbars to calibrate and press SPACE when done.'
print '	Press D to use the default settings.'
print '**********************************************************************'

yellow_range = calibrateColor('Yellow', yellow_range)
red_range = calibrateColor('Red', red_range)
blue_range = calibrateColor('Blue', blue_range)
print '	Calibration Successfull...'

cv2.namedWindow('Frame')

print '**********************************************************************'
print '	Press P to turn ON and OFF mouse simulation.'
print '	Press C to display the centroid of various colours.'
print '	Press R to recalibrate color ranges.'
print '	Press ESC to exit.'
print '**********************************************************************'
 
## setting up bluetooth com port. Make sure the ports aren't already in use
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM4' 		## need to check at device manager
ser
ser.open()

while(1):

	k = cv2.waitKey(10) & 0xFF
	changeStatus(k)


	_, frameinv = cap.read()
	# flip horizontaly to get mirror image in camera
	frame = cv2.flip( frameinv, 1)

	hsv = cv2.cvtColor( frame, cv2.COLOR_BGR2HSV)

	b_mask = makeMask( hsv, blue_range)
	r_mask = makeMask( hsv, red_range)
	y_mask = makeMask( hsv, yellow_range)

	b_cen = drawCentroid( frame, b_area, b_mask, showCentroid)
	r_cen = drawCentroid( frame, r_area, r_mask, showCentroid)	
	y_cen = drawCentroid( frame, y_area, y_mask, showCentroid)

	output = chooseAction(y_cen, r_cen, b_cen)			
	if output[0]!=-1:
		performAction(y_cen, r_cen, b_cen, output[0], output[1], perform)	
	
	cv2.imshow('Frame', frame)

	if k == 27:
		break

cv2.destroyAllWindows()
