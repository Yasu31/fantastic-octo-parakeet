#!/usr/bin/env python3
#RPi Pinouts

#I2C Pins
#GPIO2 -> SDA
#GPIO3 -> SCL

#Import the Library Requreid
from smbus2 import SMBusWrapper, i2c_msg
import time
import struct

# number of bytes we receive from Arduino
NUM_BYTES=32

# This is the address we setup in the Arduino Program
#Slave Address 1
address = 0x04

# https://github.com/kplindegaard/smbus2
# send NOUN and VERB
def writeData(noun, verb):
    bytesToSend=struct.pack('!h', noun, verb)
    with SMBusWrapper(1) as bus:
        bus.write_i2c_block_data(address, 0, bytesToSend)
    return -1

def bytes2Int(bytes):
    return int.from_bytes(bytes,byteorder='big', signed=True)

# https://docs.python.org/2/library/struct.html
# reads bytes from Arduino and return it as list of integers
def readData():
    intList=[]
    with SMBusWrapper(1) as bus:
        block=bus.read_i2c_block_data(address, 0, NUM_BYTES)
        print(block)
        # block[0:1] make up a two-byte integer, with twos complement.
        # Next, we try to convert block[] to a list of integers.
        for i in range(int(NUM_BYTES/2)):
            intList.append(bytes2Int(block[i*2:i*2+2]))
    print(intList)
    return intList


#End of the Script
