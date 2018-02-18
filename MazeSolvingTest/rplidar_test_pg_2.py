import pygame
from sys import *
from math import sin,cos,pi
from rplidar import RPLidar
lidar=RPLidar("/dev/ttyUSB0")
pygame.init()
screen=pygame.display.set_mode((500,500))
def degrees(a):
	return a*pi/180
a=0
rots=0
lastrot=0
try:
	for measurement in lidar.iter_measures(max_buf_meas=1000):
		scale=0.1
#		print(lidar.iter_measures()[-1][2])
#		last
		measurment=list(measurement)
		a=max(a,degrees(measurment[2]))
		if measurment[2]-lastrot<0 and measurment[3]!=0:
			if int(rots%1)==0:
				pygame.display.flip()
				screen.fill((0,0,0))
#				lidar.clean_input()
				pygame.draw.circle(screen,(255,0,0),(250,250),3)
				#continue
#			print(rots)
			rots+=1
#			print(rots)
#			raise KeyboardInterrupt
#			exit(0)
		if measurment[3]==0:continue# or True:
#			measurment[3]=500
#		if measurment[2]==0:continue
#        	print(measurment[3],measurment[2],a)
		if int(int(measurment[2])%90)<5:
			pygame.draw.line(screen,(0,255,255),(250,250),(int(250+measurment[3]*scale*cos(degrees(measurment[2]))),int(250-measurment[3]*scale*sin(degrees(measurment[2])))))
#		pygame.draw.circle(screen,(255,255,255),(int(250+measurment[3]/5*cos(degrees(measurment[2]))),int(250-measurment[3]/5*sin(degrees(measurment[2])))),1)
		screen.set_at((int(250+measurment[3]*scale*cos(degrees(measurment[2]))),int(250-measurment[3]*scale*sin(degrees(measurment[2])))),(255,255,255))
#        	pygame.display.flip()
		lastrot=measurment[2]
except KeyboardInterrupt:
	lidar.stop()
	lidar.stop_motor()
	lidar.disconnect()
