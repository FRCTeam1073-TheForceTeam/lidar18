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

ip = sys.argv[1]
val = 42
mmToIn = 25.4
robotSpeed=0
NetworkTables.initialize("10.10.73.2")

sd = NetworkTables.getTable("LidarSendTable")
gyroTable = NetworkTables.getTable("gyro")


print ("1073 Lidar Prototype ")


def run(path):
    '''Main function'''
    loop = False
    Inches = None
    lidarDegrees = 0
    reset = 27463478276547
    closestObject= 9144
    secondClosestObject = 9144
    PORT_NAME = '/dev/ttyUSB0'
    lidar = RPLidar(PORT_NAME)
    outfile = open(path, 'w')
    Inches1 = 10000
    Inches2 = 10000
    position1 = 0
    position2 = 0
    robotWidth = 34.752
    LidarDistancetoFront = 14.688
    LidarDistancetoBack = 25.062
    LidarDistencetoSide = 17.376
    gyroPosition = gyroTable.getNumber("gyroPosition", 99)
    try:
        print('Recording measures... Press Crl+C to stop.')
        for measurment in lidar.iter_measures():
            distance = measurment[3]
            degrees  = measurment[2]
            x = secondClosestObject
         
            if (degrees <= 185 and degrees >= 175):
                loop = True
            
            if (degrees >= 270 or degrees <= 90) and distance != 0:
                   #print '[closestObject %f]' % (closestObject)
                   #print '[degrees %f]' % (degrees)
                   #print '[distance %f]' % (distance)
                   if distance < closestObject:
                       closestObject = distance
                       position1 = degrees
                   if closestObject < distance and distance < secondClosestObject and degrees >= position1 + 18 or degrees <= position1 - 18:
                       secondClosestObject = distance
                       position2 = degrees

                   if position1 >= 0 and position1 <= 90:
                       position1 = angleRight
                       position2 = angleLeft

                   if position1 <= 360 and position2 >= 270:
                       position1 = angleLeft
                       position2 = angleRight
                       
                   if loop == True:
                       loop = False
                       Inches1 = closestObject/25.4
                       Inches2 = secondClosestObject/25.4
                       degreesBetween = position2 - position1
                       print "[inches1 %f]", (Inches1)
                       print "[inches2 %f]", (Inches2)
                       closestObject = 9144

                   if Inches1 <= 360 and Inches2 <= 360:
                       distanceBetween = math.sqrt((Inches1*Inches1)+(Inches2*Inches2)-(2*Inches1*Inches2*(math.cos(lidarDegrees))));
                       if distanceBetween >= 34.752:
                           rightAngle = 90 - angleRight
                           leftAngle = angleLeft - 270
                           baseLength1 = math.cos(rightAngle)*Inches1
                           baseLength2 = math.cos(leftAngle)*Inches2
                           
                           
                           
                           
                           
    except KeyboardInterrupt:
        print('Stopping.')
    except:
        traceback.print_exc()
        
    lidar.stop_motor()
    lidar.stop()
    lidar.disconnect()
    outfile.close()
    

if __name__ == '__main__':
    run(sys.argv[1])
