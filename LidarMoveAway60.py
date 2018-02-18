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
    lidarToBack = 23
    PORT_NAME = '/dev/ttyUSB0'
    lidar = RPLidar(PORT_NAME)
    outfile = open(path, 'w')
    ultimateMeasurement = 10909090909
    baseMeasurement = 1837.5
    
    try:
        print('Recording measures... Press Crl+C to stop.')
        for measurment in lidar.iter_measures():
            distance = measurment[3]
            degrees  = measurment[2]
            
         
            if (degrees <= 50 and degrees >= 1):
                loop = True

            if (degrees >= 150 and degrees <= 210) and distance != 0:
                if distance <= ultimateMeasurement:
                    ultimateMeasurement = distance
                    lidarDegrees = degrees
                    Inches = ultimateMeasurement/25.4 - lidarToBack
                       
                if loop == True:
                    loop = False
                    print "[inches %f]", (Inches)
                    print "Degrees", (lidarDegrees)
                    ultimateMeasurement = baseMeasurement

                if Inches <= 48:

                    if lidarDegrees > 180 and lidarDegrees <= 210:
                        turnRight = True
                        turnLeft = False
                        print "Turning Right"
                        sd.putBoolean("turnRight", turnRight)
                        sd.putBoolean("turnLeft", turnLeft)

                    elif lidarDegrees < 180 and lidarDegrees >= 150:
                        turnLeft = True
                        turnRight = False
                        print "Turning Left"
                        sd.putBoolean("turnLeft", turnLeft)
                        sd.putBoolean("turnRight", turnRight)

                    else:
                        print "Driving Sraight"
                        turnLeft = False
                        turnRight = False
                        sd.putBoolean("turnLeft", turnLeft)
                        sd.putBoolean("turnRight", turnRight)


                                           
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
