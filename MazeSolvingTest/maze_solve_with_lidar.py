import pygame
from pygame.locals import *
from rplidar import RPLidar
from math import sin,cos,pi
#from time import sleep
def sleep(a):
    pass
lidar=RPLidar("/dev/ttyUSB0")
lidar.clean_input()
lidar.start_motor()
lidar.start()
lidar.stop_motor()
lidar.stop()
def degrees(a):
	return a*pi/180

pygame.init()
WIDTH=600
HEIGHT=600
screen=pygame.display.set_mode((WIDTH*2,HEIGHT))
def scanWalls(closeDist,farDist):
	a=0
	rots=0
	lastrot=0
	maxloops=300
	loops=0
	screen2=pygame.Surface((500,500))
	north=[]
	south=[]
	east=[]
	west=[]
	for measurement in lidar.iter_measures(max_buf_meas=1000):
		scale=0.125
#		print(lidar.iter_measures()[-1][2])
#		last
		measurment=list(measurement)
		a=max(a,degrees(measurment[2]))
		if measurment[2]-lastrot<0 and measurment[3]!=0:
			if int(rots%1)==0:
				if loops==maxloops:break
				loops+=1
				pygame.display.flip()
				screen2.fill((0,0,0))
#				lidar.clean_input()
				pygame.draw.circle(screen2,(255,0,0),(250,250),3)
				#continue
#			print(rots)
			rots+=1
#			print(rots)
#			raise KeyboardInterrupt
#			exit(0)
		WIDTH=5
		if measurment[3]==0:continue# or True:
#			measurment[3]=500
#		if measurment[2]==0:continue
#        	print(measurment[3],measurment[2],a)
		if 360-WIDTH<(measurment[2]%360) or (measurment[2]%360)<WIDTH:
#		if int(int(measurment[2])%90)<5:
			print("RED")
			pygame.draw.line(screen2,(255,0,0),(250,250),(int(250+measurment[3]*scale*cos(degrees(measurment[2]))),int(250-measurment[3]*scale*sin(degrees(measurment[2])))))
			north.append(measurment[3])
		elif ((90-WIDTH)%360)<measurment[2]<((90+WIDTH)%360):
#		if int(int(measurment[2])%90)<5:
			print("GREEN")
			pygame.draw.line(screen2,(0,255,0),(250,250),(int(250+measurment[3]*scale*cos(degrees(measurment[2]))),int(250-measurment[3]*scale*sin(degrees(measurment[2])))))
			west.append(measurment[3])
		elif ((180-WIDTH)%360)<measurment[2]<((180+WIDTH)%360):
#		if int(int(measurment[2])%90)<5:
			print("YELLOW")
			pygame.draw.line(screen2,(255,255,0),(250,250),(int(250+measurment[3]*scale*cos(degrees(measurment[2]))),int(250-measurment[3]*scale*sin(degrees(measurment[2])))))
			south.append(measurment[3])
		elif ((270-WIDTH)%360)<measurment[2]<((270+WIDTH)%360):
#		if int(int(measurment[2])%90)<5:
			print("BLUE")

			pygame.draw.line(screen2,(0,0,255),(250,250),(int(250+measurment[3]*scale*cos(degrees(measurment[2]))),int(250-measurment[3]*scale*sin(degrees(measurment[2])))))
			east.append(measurment[3])
#		pygame.draw.circle(screen,(255,255,255),(int(250+measurment[3]/5*cos(degrees(measurment[2]))),int(250-measurment[3]/5*sin(degrees(measurment[2])))),1)
		screen2.set_at((int(250+measurment[3]*scale*cos(degrees(measurment[2]))),int(250-measurment[3]*scale*sin(degrees(measurment[2])))),(255,255,255))
#        	pygame.display.flip()
		lastrot=measurment[2]
		screen.blit(screen2,(WIDTH,0))
	lidar.stop()
	lidar.stop_motor()
	lidar.clean_input()
	lidar.disconnect()
    
class Robot:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.px=x
        self.py=y
        self.facing="north"
        self.pathstring=""
        self.size=20
        self.facing_vectors={
            "north":(0,-1),
            "south":(0,1),
            "east":(1,0),
            "west":(-1,0),
        }
        self.opposites={
            "north":"south",
            "south":"north",
            "east":"west",
            "west":"east"
        }
        self.rights={"north":"west",
               "west":"south",
               "south":"east",
               "east":"north"}
        self.lefts={"north":"east",
               "east":"south",
               "south":"west",
               "west":"north"}
        self.rotmatrix={"forward":{"north":"north","east":"east","south":"south","west":"west"},
                        "backward":{"north":"south","east":"west","south":"north","west":"east"},
                        "left":{"north":"west","east":"north","south":"east","west":"south"},
                        "right":{"north":"east","east":"south","south":"west","west":"north"}
                        }
                        
        self.lastMove=self.facing
    def moveStep(self):
        north,east,south,west=self.scan()
        possibleDirections=[]
        if not north:possibleDirections.append("north")
        if not south:possibleDirections.append("south")
        if not east:possibleDirections.append("east")
        if not west:possibleDirections.append("west")
        if len(possibleDirections)==4 and (self.x<0 or self.y<0 or self.x>gridAmount or self.y>gridAmount):
            #print("I escaped!!")
            return "ESCAPED"
        if len(possibleDirections)>2 and (self.facing in possibleDirections) and (not (self.lefts[self.facing] in possibleDirections)):
            #print("Spof")
            self.moveForward()
            return
        if len(possibleDirections)==2 and self.lastMove in possibleDirections and self.opposites[self.lastMove] in possibleDirections:
            self.moveForward()
            return
        if len(possibleDirections)==2 and self.rights[self.lastMove] in possibleDirections and self.opposites[self.lastMove] in possibleDirections:
            self.rotateLeft()
            self.moveForward()
            return
        if len(possibleDirections)==2 and self.lefts[self.lastMove] in possibleDirections and self.opposites[self.lastMove] in possibleDirections:
            self.rotateRight()
            self.moveForward()
            return
        if possibleDirections==[self.opposites[self.lastMove]]:
            self.rotateLeft()
            self.rotateLeft()
            self.moveForward()
            return
        #for dr in possibleDirections:
            #print("I can go "+dr.upper())
##        #print("But I last went "+self.lastMove.upper()+", so I can't go "+self.opposites[self.lastMove].upper()+" this time.")
##        if self.opposites[self.lastMove] in possibleDirections:
##            possibleDirections.remove(self.opposites[self.lastMove])
        #print("Turning backwards:")
        self.rotateRight()
        while True:
            if self.facing in possibleDirections:
                #print("I found a path!")
                self.moveForward()
                return
            self.rotateLeft()
    def moveForward(self):
        length=50
        for extra_amt in range(length):
            extra=extra_amt/float(length)
            screen.fill((0,0,0))
            drawGrid()
            pygame.draw.rect(screen,(255,0,0),((self.x+self.facing_vectors[self.facing][0]*extra)*gridSize[0]+gridSize[0]//2-self.size//2,
                                               (self.y+self.facing_vectors[self.facing][1]*extra)*gridSize[1]+gridSize[1]//2-self.size//2,
                                               self.size,
                                               self.size))
            pygame.display.flip()
        self.x+=self.facing_vectors[self.facing][0]
        self.y+=self.facing_vectors[self.facing][1]
        self.lastMove=str(self.facing)
        self.display()
        self.pathstring=self.pathstring+"F"
    def recallPath(self):
        self.facing="north"
        #print("Recalling...")
        self.x=self.px*1
        self.y=self.py*1
        for path in list(self.pathstring):
            if path=="R":
                self.rotateRight()
            if path=="L":
                self.rotateLeft()
            if path=="F":
                self.moveForward()
    def scan(self):
        north=False
        south=False
        east=False
        west=False
        for line in walls:
            if min(line[0][1],line[1][1])<=self.y and max(line[0][1],line[1][1])>self.y:
                if line[0][0]==line[1][0] and line[0][0]>self.x:
                    if line[0][0]==self.x+1:
                        east=True
                        #print("EAST")
                        #print(line)
                if line[0][0]==line[1][0] and line[0][0]<=self.x:
                    if line[0][0]==self.x:
                        west=True
                        #print("WEST")
                        #print(line)
            if min(line[0][0],line[1][0])<=self.x and max(line[0][0],line[1][0])>self.x:
                if line[0][1]==line[1][1] and line[0][1]>self.y:
                    if line[0][1]==self.y+1:
                        south=True
                        #print("SOUTH")
                        #print(line)
                if line[0][1]==line[1][1] and line[0][1]<=self.y:
                    if line[0][1]==self.y:
                        north=True
                        #print("NORTH")
                        #print(line)
        sleep(0.25)
        self.display()
        if east:
            pygame.draw.line(screen,(0,255,255),
                             (self.x*gridSize[0]+gridSize[0]//2,
                              self.y*gridSize[1]+gridSize[1]//2),
                             (self.x*gridSize[0]+gridSize[0]//2+50,
                              self.y*gridSize[1]+gridSize[1]//2))
            pygame.display.flip()
            sleep(0.25)
        if west:
            pygame.draw.line(screen,(0,255,255),
                             (self.x*gridSize[0]+gridSize[0]//2,
                              self.y*gridSize[1]+gridSize[1]//2),
                             (self.x*gridSize[0]+gridSize[0]//2-50,
                              self.y*gridSize[1]+gridSize[1]//2))
            pygame.display.flip()
            sleep(0.25)
        if south:
            pygame.draw.line(screen,(0,255,255),
                             (self.x*gridSize[0]+gridSize[0]//2,
                              self.y*gridSize[1]+gridSize[1]//2),
                             (self.x*gridSize[0]+gridSize[0]//2,
                              self.y*gridSize[1]+gridSize[1]//2+50))
            pygame.display.flip()
            sleep(0.25)
        if north:
            pygame.draw.line(screen,(0,255,255),
                             (self.x*gridSize[0]+gridSize[0]//2,
                              self.y*gridSize[1]+gridSize[1]//2),
                             (self.x*gridSize[0]+gridSize[0]//2,
                              self.y*gridSize[1]+gridSize[1]//2-50))
            pygame.display.flip()
            sleep(0.25)
##        if self.facing=="north":
##            return [north,east,south,west]
##        if self.facing=="south":
##            return [south,west,north,east]
##        if self.facing=="west":
##            return [west,north,east,south]
##        if self.facing=="east":
##            return [east,south,west,north]
        return [north,east,south,west]
    def display(self):
        pygame.draw.rect(screen,(255,0,0),(self.x*gridSize[0]+gridSize[0]//2-self.size//2,
                                           self.y*gridSize[1]+gridSize[1]//2-self.size//2,
                                           self.size,
                                           self.size))
        pygame.draw.line(screen,(255,255,0),(self.x*gridSize[0]+gridSize[0]//2,
                                             self.y*gridSize[1]+gridSize[1]//2),
                                            (self.x*gridSize[0]+gridSize[0]//2+self.facing_vectors[self.facing][0]*50,
                                             self.y*gridSize[1]+gridSize[1]//2+self.facing_vectors[self.facing][1]*50),
                                             2) 
        pygame.display.flip()
    def rotateRight(self):
        angle={"north":90,
               "south":270,
               "east":0,
               "west":180}[self.facing]*1
        ang=2
        for x in range(90/ang):
            angle-=ang
            screen.fill((0,0,0))
            drawGrid()
            surf=pygame.Surface(gridSize[:],SRCALPHA,32)
            pygame.draw.rect(surf,(255,0,0),(gridSize[0]//2-self.size//2,gridSize[1]//2-self.size//2,self.size,self.size))
            pygame.draw.line(surf,(255,255,0),(gridSize[0]//2,gridSize[1]//2),(gridSize[0],gridSize[1]//2),2)
            surf2=pygame.transform.rotate(surf,angle)
            screen.blit(surf2,(self.x*gridSize[0]+gridSize[0]//2-surf2.get_rect()[2]//2,self.y*gridSize[1]+gridSize[1]//2-surf2.get_rect()[3]//2))
            pygame.display.flip()
        self.facing={"north":"east",
               "east":"south",
               "south":"west",
               "west":"north"}[self.facing]
        self.pathstring=self.pathstring+"R"
    def rotateLeft(self):
        angle={"north":90,
               "south":270,
               "east":0,
               "west":180}[self.facing]*1
        ang=2
        for x in range(90/ang):
            angle+=ang
            screen.fill((0,0,0))
            drawGrid()
            surf=pygame.Surface(gridSize[:],SRCALPHA,32)
            pygame.draw.rect(surf,(255,0,0),(gridSize[0]//2-self.size//2,gridSize[1]//2-self.size//2,self.size,self.size))
            pygame.draw.line(surf,(255,255,0),(50,50),(100,50),2)
            surf2=pygame.transform.rotate(surf,angle)
            screen.blit(surf2,(self.x*gridSize[0]+gridSize[0]//2-surf2.get_rect()[2]//2,self.y*gridSize[1]+gridSize[1]//2-surf2.get_rect()[3]//2))
            pygame.display.flip()
        self.facing={"north":"west",
               "west":"south",
               "south":"east",
               "east":"north"}[self.facing]
        self.pathstring=self.pathstring+"L"
#print("S")
def drawGrid():
    return
    for x in range(0,600,gridSize[0]):
        pygame.draw.line(screen,(155,155,155),(x,0),(x,HEIGHT),1)
    #    pygame.display.flip()
    for y in range(0,600,gridSize[1]):
        pygame.draw.line(screen,(155,155,155),(0,y),(WIDTH,y),1)
    #    pygame.display.flip()
    for line in walls:
        pygame.draw.line(screen,(255,255,255),(line[0][0]*gridSize[0],
                                               line[0][1]*gridSize[1]),
                                              (line[1][0]*gridSize[0],
                                               line[1][1]*gridSize[1]),3)
    #pygame.display.flip()
gridAmount=12
gridSize=[WIDTH//gridAmount,HEIGHT//gridAmount]
##gridString="""\
##000000
##000000
##000000
##000000
##000000
##000000"""
##gridTilesTemp=gridString.splitlines()
##gridTiles=list(list(gs) for gs in gridTilesTemp)
walls=[
[[0, 0], [11, 0]],
[[12, 0], [12, 12]],
[[0, 12], [12, 12]],
[[1, 0], [1, 7]],
[[1, 4], [2, 4]],
[[1, 6], [7, 6]],
[[2, 4], [2, 5]],
[[2, 5], [6, 5]],
[[6, 5], [6, 3]],
[[6, 3], [6, 1]],
[[6, 3], [8, 3]],
[[6, 1], [4, 1]],
[[7, 0], [7, 2]],
[[7, 2], [8, 2]],
[[8, 2], [8, 3]],
[[8, 1], [9, 1]],
[[9, 1], [9, 2]],
[[9, 2], [11, 2]],
[[10, 1], [11, 1]],
[[11, 1], [11, 0]],
[[11, 2], [11, 3]],
[[11, 3], [9, 3]],
[[9, 3], [9, 5]],
[[9, 5], [8, 5]],
[[7, 6], [7, 4]],
[[7, 4], [8, 4]],
[[8, 5], [8, 6]],
[[9, 6], [10, 6]],
[[8, 6], [9, 6]],
[[9, 6], [9, 7]],
[[9, 7], [7, 7]],
[[7, 7], [7, 8]],
[[7, 8], [6, 8]],
[[6, 8], [6, 7]],
[[6, 7], [2, 7]],
[[2, 7], [2, 8]],
[[2, 8], [1, 8]],
[[1, 8], [1, 9]],
[[1, 9], [2, 9]],
[[2, 9], [2, 10]],
[[2, 10], [1, 10]],
[[1, 11], [3, 11]],
[[3, 11], [3, 10]],
[[3, 10], [5, 10]],
[[4, 10], [4, 9]],
[[4, 9], [3, 9]],
[[3, 9], [3, 8]],
[[3, 8], [2, 8]],
[[5, 12], [5, 11]],
[[5, 11], [4, 11]],
[[5, 10], [5, 9]],
[[4, 7], [4, 8]],
[[4, 8], [5, 8]],
[[7, 8], [7, 10]],
[[7, 10], [6, 10]],
[[6, 10], [6, 9]],
[[7, 10], [11, 10]],
[[11, 10], [11, 11]],
[[9, 10], [9, 11]],
[[6, 12], [6, 11]],
[[6, 11], [7, 11]],
[[7, 11], [7, 12]],
[[8, 12], [8, 11]],
[[10, 12], [10, 11]],
[[8, 9], [12, 9]],
[[8, 9], [8, 8]],
[[8, 8], [9, 8]],
[[10, 9], [10, 8]],
[[10, 8], [11, 8]],
[[10, 6], [10, 7]],
[[10, 7], [11, 7]],
[[11, 6], [12, 6]],
[[11, 4], [11, 5]],
[[10, 4], [12, 4]],
[[10, 4], [10, 6]],
[[5,11],[6,11]]
]
scanWalls(0,0)
robot=Robot(5,10)
drawGrid()
robot.display()
pygame.display.flip()
clock=pygame.time.Clock()
while True:
    s=robot.moveStep()
    
    if s=="ESCAPED":break
    #clock.tick(30)
#robot.recallPath()
