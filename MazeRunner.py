import time
import sys

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


def run(path):
    '''Main function'''
    loop = False
    Inches = None
    lidarDegrees = 0
    reset = 27463478276547
    baseMeasurement= 2540
    ultimateMeasurement = 6400
    PORT_NAME = '/dev/ttyUSB0'
    lidar = RPLidar(PORT_NAME)
    outfile = open(path, 'w')
    #ZeroBlocked = False
    #NinetyBlocked= False
    #OneEightyBlocked = False
    #TwoSeventyBlocked = False
    
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
                   if distance <= ultimateMeasurement:
                       ultimateMeasurement = distance
                       lidarDegrees = degrees
                       
                   if loop == True:
                       loop = False
                       Inches = ultimateMeasurement/25.4
                       print "[inches %f]", (Inches)
                       ultimateMeasurement = baseMeasurement

                       if Inches is None:
                           continue
                       #note: in all situations below, left should be listed above right
                       if Inches <= 100:

                           robotSpeed = (0.00005018*(Inches*Inches))+0.1
                       elif Inches > 100:
                           robotSpeed = 0.5
                       print ("robotSpeed", robotSpeed)
                       if lidarDegrees > 270 and lidarDegrees < 355 and Inches > 12: 
                           left = robotSpeed
                           right = robotSpeed + 0.1
                       elif lidarDegrees > 5 and lidarDegrees < 90 and Inches > 12:
                           left = robotSpeed + 0.1
                           right = robotSpeed
                       elif lidarDegrees >= 90 and lidarDegrees < 175 and Inches > 12:
                           left = -1*(robotSpeed + 0.1)
                           right = robotSpeed
                       elif lidarDegrees > 185 and lidarDegrees < 270 and Inches > 12 :
                           left = robotSpeed 
                           right = -1* (robotSpeed + .1)
                       elif lidarDegrees >= 175 and lidarDegrees <= 185 and Inches >= 36:
                           left = -1*robotSpeed
                           right = -1*robotSpeed
                           print ("back", robotSpeed)
                       elif lidarDegrees >= 355 and lidarDegrees <=5 and Inches >= 12:
                           left = robotSpeed
                           right = robotSpeed
                       elif Inches <= 6 and lidarDegrees >= 270 and lidarDegrees <= 90:
                            print 'stopped'
                            right = 0
                            left = 0
                       elif Inches <= 36 and lidarDegrees >= 90 and lidarDegrees <= 270:
                            print 'stopped'
                            right = 0
                            left = 0
                       else:
                            left = 0.5
                            right = 0.5

                        #if degrees >= 
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
    lidar.stop_motor()
    lidar.stop()
    lidar.disconnect()
    outfile.close()

if __name__ == '__main__':
    run(sys.argv[1])
