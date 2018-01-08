#!/usr/bin/env python3
# pip3 install pyYAML
# pip3 install rospkg
# pip3 install catkin_pkg
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Int32, Float64
#RPi Pinouts
#I2C Pins
#GPIO2 -> SDA
#GPIO3 -> SCL

######## code for I2C communication ########
#Import the Library Requreid
#from smbus2 import SMBusWrapper, i2c_msg
from smbus import SMBus
import time
import struct

# number of bytes we receive from Arduino
NUM_BYTES=14

# This is the address we setup in the Arduino Program
#Slave Address 1
address = 0x04

bus=SMBus(1)

# https://github.com/kplindegaard/smbus2
# send NOUN and VERB
def writeData(noun, verb):
    bytesToSend=struct.pack('!hh', noun, verb)
    global bus
    if True:
        bus.write_i2c_block_data(address, 0, list(bytesToSend))
    return -1

def bytes2Int(bytes):
    # only available in Python3
    return int.from_bytes(bytes,byteorder='big', signed=True)

# https://docs.python.org/2/library/struct.html
# reads bytes from Arduino and return it as list of integers
def readData():
    intList=[]
    global bus
    if True:
        block=bus.read_i2c_block_data(address, 0)#, NUM_BYTES)
        #print(block)
        # block[0~1] make up a two-byte integer, with twos complement.
        # block[2~3] is the same, too (and so on)
        # So, we try to convert block[] to a list of integers.
        for i in range(int(NUM_BYTES/2)):
            intList.append(bytes2Int(block[i*2:i*2+2]))
    #print(intList)
    return intList

######## END OF code for I2C communication ########

corrections=[-1,1,-1,1,-1,-1,1]
def publishSensors():
    pub=rospy.Publisher('joint_states', JointState, queue_size=10)

    audioPub=rospy.Publisher('audio', Int32, queue_size=10)
    audioPub.init_node('talker', anonymous=True)

    rospy.init_node('joint_state_publisher_a', anonymous=True)
    rate=rospy.Rate(10)
    jointState=JointState()
    time.sleep(1)
    audioPub.publish(2)
    while not rospy.is_shutdown():
        try:
            sensorInfos=readData()
            for i in range(len(sensorInfos)):
                sensorInfos[i]*=corrections[i]
        except:
            print("error received... moving on")
        jointNames=[]
        for i in range(7):
            jointNames.append("link"+str(i)+"_link"+str(i+1)+"_joint")
        jointState.header.stamp=rospy.Time.now()
        jointState.name=jointNames
        # angles are in degrees*100. Convert to radians

        jointState.position=[i/100*3.1415/180 for i in sensorInfos]

        jointState.velocity=[]
        jointState.effort=[]
        pub.publish(jointState)
        rate.sleep()

def callback(data):
    # output stuff to robot...
    pass

if __name__ == '__main__':
    try:
        rospy.init_node('node', anonymous=True)
        rospy.Subscriber("??", Float64, callback)
        publishSensors()
    except rospy.ROSInterruptException:
        pass
