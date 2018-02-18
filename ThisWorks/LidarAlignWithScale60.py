import time
import sys
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


def run(path):
    '''Main function'''
    loop = False
    Inches = None
    lidarDegrees = 0
    reset = 27463478276547
    baseMeasurement= 18000
    ultimateMeasurement = 6400
    PORT_NAME = '/dev/ttyUSB0'
    lidar = RPLidar(PORT_NAME)
    outfile = open(path, 'w')
    stop = False
    lidarToBack = 33
    try:
        print('Recording measures... Press Crl+C to stop.')
        for measurment in lidar.iter_measures():
            distance = measurment[3]
            degrees  = measurment[2]
         
            if (degrees <= 149 or degrees >= 211):
                loop = True
            
            if (degrees >= 150 and degrees <= 210) and distance != 0:
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
                       Inches = (ultimateMeasurement/25.4) - lidarToBack
                       print "[inches %f]", (Inches)
                       ultimateMeasurement = baseMeasurement

                       if Inches is None:
                           continue
                       #note: in all situations below, left should be listed above right
                       if Inches <= 18:
                           stop = True
                           sd.putBoolean("Stop", stop)
                           print("Boolean Stop is True")
                       else:
                           stop = False
                           sd.putBoolean("Stop", stop)
                           print("Boolean Stop is False")

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
    run(sys.argv[1])
