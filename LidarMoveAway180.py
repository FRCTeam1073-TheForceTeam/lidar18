import time
import sys
import math
import traceback
from time import sleep

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


def LidarMoveAway360(path):
    '''Main function'''
    loop = False
    Inches = None
    lidarDegrees = 0
    reset = 27463478276547
    stop = False
    turnLeft = False
    turnRight = False
    lidarToBack = 33
    PORT_NAME = '/dev/ttyUSB0'
    lidar = RPLidar(PORT_NAME)
    outfile = open(path, 'w')
    ultimateMeasurement = 10909090909
    baseMeasurement = 1837.5
    position = 0
    p1dist = 0
    p1deg = 0
    p2dist = 0
    p2deg = 0
    deltadist = 0 
    deltadeg = 0
    moving = "center"
    FirstDeg = 0
    

    try:
        print('Recording measures... Press Crl+C to stop.')
        for measurment in lidar.iter_measures():
            distance = measurment[3]
            degrees  = measurment[2]
            
         
            if (degrees <= 50 and degrees >= 1):
                loop = True
                

            if (degrees >= 90 and degrees <= 270) and distance != 0:
                if distance <= ultimateMeasurement:
                    ultimateMeasurement = distance
                    lidarDegrees = degrees
                    p1deg = degrees                    
                    print("HERE", p1deg)

                    if loop == True:
                        loop = False
                        Inches = ultimateMeasurement/25.4 - lidarToBack
                        print "[inches %f]", (Inches)
                        ultimateMeasurement = baseMeasurement
                        FirstDeg = p1deg
                        p1deg = 0
                        print("NOW", FirstDeg)
                        

                    if Inches <= 48:
                       
                        if deltadeg > 2 :
                            moving = "left"
                        if deltadeg < -1:
                            moving = "right"
                        
                        print("deltadeg", deltadeg)
                        
                        if moving == "right":
                            #position = 2
                            #turnRight = True
                            #print "Turning Right"
                            #sd.putBoolean("turnRight", turnRight)
                            #sd.putNumber("position", position)
                            turnLeft = True
                            print "Turning Left"
                            sd.putBoolean("turnLeft", turnLeft)
                            
                        if moving =="left":
                           # position = 1
                            turnRight = True
                            print "Turning Right"
                            sd.putBoolean("turnRight", turnRight)
                            sd.putNumber("position", position)
            
                                      
    except KeyboardInterrupt:
        print('Stopping.')
    except:
        traceback.print_exc()
        
    lidar.stop_motor()
    lidar.stop()
    lidar.disconnect()
    outfile.close()
    

if __name__ == '__main__':
    LidarMoveAway360(sys.argv[1])
    #sd.AddTableListener(LidarMoveAway360)
