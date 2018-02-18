import time
import sys
import math
import traceback

from rplidar import RPLidar
from networktables import NetworkTables
PORT_NAME = '/dev/ttyUSB0'
# To see messages from networktables, you must setup logging
import logging
logging.basicConfig(level=logging.ERROR)

if len(sys.argv) != 2:
    print("Error: specify an IP to connect to!")
    exit(0)

NetworkTables.initialize("10.10.73.2")

sd = NetworkTables.getTable("LidarSendTable")




ip = sys.argv[1]
val = 42
mmToIn = 25.4
state = sd.getNumber("lidarState", 0.0)
robotSpeed=0
loop = False
Inches = None
lidarDegrees = 0
reset = 27463478276547
baseMeasurement= 2540
ultimateMeasurement = 6400
PORT_NAME = '/dev/ttyUSB0'
LidarDistancetoFront = 14.688
LidarDistancetoBack = 25.062
LidarDistencetoSide = 17.376
measure1 = 0
measure2 = 0
measure3 = 0
state = 0




print ("1073 Lidar Prototype ")

try:
    def Init(path):
        lidar = RPLidar(PORT_NAME)
        outfile = open(path, 'w')
        degrees = measurment[2]
        distance = measurment[3] 
    def LidarAlignToWall(path):
            '''Main function'''
        
        if (degrees <= 185 and degrees >= 175):
            loop = True
            
        if (degrees >= 265 or degrees <= 90) and distance != LidarDistancetoSide:
            if distance <= ultimateMeasurement:
                ultimateMeasurement = distance
                lidarDegrees = degrees
                       
            if loop == True:
                loop = False
                Inches = ultimateMeasurement/25.4
                print "[inches %f]", (Inches)
                ultimateMeasurement = baseMeasurement

            #note: in all situations below, left should be listed above right
            if Inches <= 100:
                robotSpeed = (0.00005018*(Inches*Inches))+0.1
            elif Inches > 100:
                robotSpeed = 0.5
                print ("robotSpeed", robotSpeed)
            if (lidarDegrees > 270 and lidarDegrees < 355) and Inches > 25:
                print "leftFront"
                left = robotSpeed
                right = robotSpeed + 0.1
            elif lidarDegrees > 5 and lidarDegrees < 90 and Inches > 25:
                left = robotSpeed + 0.1
                right = robotSpeed
                           
            elif (lidarDegrees >= 355 or lidarDegrees <=5) and Inches >= 25:
                print "front"
                left = robotSpeed
                right = robotSpeed
            elif (lidarDegrees >= 358 or lidarDegrees <= 93) and Inches >= 25:
                print "rightFront"
                left = robotSpeed + 0.1
                right = robotSpeed
            elif Inches <= 25 and (lidarDegrees >= 270 or lidarDegrees <= 90):
                 print 'stopped'
                 right = 0
                 left = 0
            else:
                left = 0.5
                right = 0.5
                            
            sd.putNumber("left", left)
            sd.putNumber("right", right)
            sd.putNumber("Inches", Inches)
            print ("lidarDegrees", lidarDegrees)
            print ("right", right)
            print ("left", left)

    def LidarRecognizeWall(path):
        if lidarDegrees >= 337 and lidarDegrees <= 343:
            distA = Inches
            degA = lidarDegrees
            measure1 = distA*math.sin(degA)
            print("measure1", measure1)
        if lidarDegrees >=358 or lidarDegrees <=2:
            distB = Inches
            degB = lidarDegrees
            measure2 = distB*math.sin(degB)
            print("measure2", measure2)
        if lidarDegrees >= 28 and lidarDegrees <= 32 :
            distC = Inches
            degC = lidarDegrees
            measure3 = distC*math.sin(degC)
            print("measure3", measure3)
        if Inches <= 25 and((measure2 - measure1 <= 2 or measure2 - measure1 >= -2) and (measure2 - measure3 <= 2 or measure2 - measure3 >= -2) and (measure1 - measure3 <= 2 or measure1 -measure3 >= -2)):
            sd.putString("Turn", "turn")

            if lidarDegrees > 87 and lidarDegrees < 93 and Inches < 26: 
                left = robotSpeed
                right = robotSpeed + 0.1
            if (degrees >= 357 or degrees <= 3) and Inches <= 30:
                center = Inches
                print("center", center)
                sd.putNumber("center", center)
                                   
            elif degrees >= 87 and degrees <= 93 and Inches <= 30:
                rightSide = Inches
                print("rightSide", rightSide)
                sd.putNumber("rightSide", rightSide)

            elif (degrees >= 267 or degrees <= 3) and Inches <= 30:
                leftSide = Inches
                print("leftSide", leftSide)
                sd.putNumber("leftSide", leftSide)
        
            elif lidarDegrees < 272 and lidarDegrees > 268 and Inches < 26:
                left = robotSpeed + 0.1
                right = robotSpeed
                if (degrees >= 357 or degrees <= 3) and Inches <= 30:
                    center = Inches
                    print("center", center)
                    sd.putNumber("center", center)
                                   
                elif degrees >= 87 and degrees <= 93 and Inches <= 30:
                    rightSide = Inches
                    print("rightSide", rightSide)
                    sd.putNumber("rightSide", rightSide)
                                   
                elif (degrees >= 267 or degrees <= 3) and Inches <= 30:
                    leftSide = Inches
                    print("leftSide", leftSide)
                    sd.putNumber("leftSide", leftSide)
                                   
                else:
                    left = 0.3
                    right = 0.3
    
    def LidarMoveAlongWall(path):
        leftOrRight = sd.getString("Turn", "turn")
        if leftOrRight == "left":
            print ("leftOrRight", leftOrRight)
            if lidarDegrees < 92 and lidarDegrees > 88 and Inches > 24: 
                right = robotSpeed
                if (degrees >= 357 or degrees <= 3) and Inches <= 30:
                    center = Inches
                    print("center", center)
                    sd.putNumber("center", center)
                elif degrees >= 87 and degrees <= 93 and Inches <= 30:
                    rightSide = Inches
                    print("rightSide", rightSide)
                    sd.putNumber("rightSide", rightSide)

                elif (degrees >= 267 or degrees <= 3) and Inches <= 30:
                    leftSide = Inches
                    print("leftSide", leftSide)
                    sd.putNumber("leftSide", leftSide)

                elif lidarDegrees < 92 and lidarDegrees > 88 and Inches < 26:
                    left = robotSpeed 
                    right = robotSpeed + 0.1
                                   
                if (degrees >= 357 or degrees <= 3) and Inches <= 30:
                    center = Inches
                    print("center", center)
                    sd.putNumber("center", center)
                                   
                elif degrees >= 87 and degrees <= 93 and Inches <= 30:
                    rightSide = Inches
                    print("rightSide", rightSide)
                    sd.putNumber("rightSide", rightSide)

                elif (degrees >= 267 or degrees <= 3) and Inches <= 30:
                    leftSide = Inches
                    print("leftSide", leftSide)
                    sd.putNumber("leftSide", leftSide)

                else:
                    left = 0.3
                    right = 0.3
                

                           

                           

                                
except KeyboardInterrupt:
    print('Stopping.')
except:
    traceback.print_exc()
        
lidar.stop_motor()
lidar.stop()
lidar.disconnect()
outfile.close()

if __name__ == '__main__':
    if state == 0:
        Init(sys.argv[1])
    if state == 1: 
        LidarAlignToWall(sys.argv[1])
    if state == 2:
        LidarRecognizeWall(sys.argv[1])
    if state == 3:
        LidarMoveAlongWall(sys.argv[1])
        
