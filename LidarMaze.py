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


def LidarAlign360(path):
    '''Main function'''
    loop = False
    Inches = None
    lidarDegrees = 0
    reset = 10
    baseMeasurement= 3000
    ultimateMeasurement = 10
    PORT_NAME = '/dev/ttyUSB0'
    lidar = RPLidar(PORT_NAME)
    outfile = open(path, 'w')
    ZeroBlocked = False
    NinetyBlocked = False
    OneEightyBlocked = False
    TwoSeventyBlocked = False
    try:
        print('Recording measures... Press Crl+C to stop.')
        for measurment in lidar.iter_measures():
            distance = measurment[3]
            degrees  = measurment[2]

         
            if (degrees <= 185 and degrees >= 175):
                loop = True
            
            if (degrees >= 0 or degrees <= 360) and distance != 0:
                   #print '[ultimateMeasurement %f]' % (ultimateMeasurement)
                   #print '[degrees %f]' % (degrees)
                   #print '[distance %f]' % (distance)
                   #if distance < baseMeasurement:
                       #ultimateMeasurement = distance
                   if(degrees >= 358 and degrees <= 2):
                   if distance >= ultimateMeasurement:
                       ultimateMeasurement = distance
                       lidarDegrees = degrees
                       
                   if loop == True:
                       loop = False
                       Inches = ultimateMeasurement/25.4
                       print "[inches %f]", (Inches)
                       ultimateMeasurement = baseMeasurement
                       
                       
                   if (degrees >= 358 or degrees <= 2) and Inches <= 10:
                       ZeroBlocked = True;
                   elif (degrees >= 88 and degrees <= 92) and Inches <= 10:
                       NinetyBlocked = True;
                   elif (degrees >= 178 and degrees <= 182) and Inches <= 10:
                       OneEightyBlocked = True
                   elif (degrees >= 268 and degrees <= 272) and Inches < = 10:
                       TwoSeventyBlocked = True
                   else:
                       ZeroBlocked = False
                       NinetyBlocked = False
                       OneEightyBlocked = False
                       TwoSeventyBlocked = False
                       
                   if ZeroBlocked == False and NinetyBlocked == True and TwoSeventyBlocked == True:
                       sd.putDouble("MazeSpeed", 0.5)
                   if OneEightyBlocked = False and ZeroBlocked == True and NinetyBlocked = True and TwoSeventyBlocked = True:
                       sd.putDouble("MazeSpeed", -0.5)
                   if      
                       

                   
                       sd.putNumber("left", left)
                       sd.putNumber("right", right)
                       print ("lidarDegrees", lidarDegrees)
                       print ("right", right)
                       print ("left", left)
                       #print'[robotSpeed = %f]' % (robotSpeed) 
                       #sd.putNumber('ultimateMeasurement', ultimateMeasurement)
                   #if loop == True:    
                       #ultimateMeasurement = baseMeasurement
        
        
         
                
        
                   
               
    except KeyboardInterrupt:
        print('Stopping.')
    except:
        traceback.print_exc()
        
    lidar.stop_motor()
    lidar.stop()
    lidar.disconnect()
    outfile.close()

if __name__ == '__main__':
    LidarAlign360(sys.argv[1])
    sd.AddTableListener(LidarAlign360)

    #if 
