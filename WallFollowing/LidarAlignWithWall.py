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
        state = 1
        
       
    def LidarCenterToWall(path):
            '''Main function'''
        if degrees == 0 && distance != 0:
            center = distance/25.4
            

        if degrees == 60 && distance != 0:
            right = distance/25.4

        if degrees == 300 && distance != 0:
            left = distance/25.4
            
        robotSpeed = (0.00005018*(center*center))+0.1
        if center >= 5:
            if left > right:
                leftSpeed = robotSpeed
                rightSpeed = robotSpeed + 0.1

            elif left < right:
                leftSpeed = robotSpeed
                rightSpeed = robotSpeed + 0.1

            else:
                leftSpeed = robotSpeed
                rightSpeed = robotSpeed
        else:
            leftSpeed = 0
            rightSpeed = 0
            state = 2

        sd.putNumber("leftSpeed", leftSpeed)
        sd.putNumber("rightSpeed", rightSpeed)
        
    def FindWall(path):
         if (left >= (center + 10) <= right) and (:

        
            

                                
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
        
