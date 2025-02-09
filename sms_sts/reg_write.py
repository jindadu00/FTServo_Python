#!/usr/bin/env python
#
# *********     Gen Write Example      *********
#
#
# Available SCServo model on this example : All models using Protocol SCS
# This example is tested with a SCServo(STS/SMS), and an URT
#

import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from scservo_sdk import *                      # Uses FTServo SDK library

IDLIST = [1, 2, 3]


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler('COM3')# ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

# Initialize PacketHandler instance
# Get methods and members of Protocol
packetHandler = sms_sts(portHandler)
    
# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()

# Set port baudrate 1000000
if portHandler.setBaudRate(1000000):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()

for scs_id in IDLIST:
    scs_comm_result, scs_error = packetHandler.ServoMode(scs_id)
    if scs_comm_result != True:
        print("[ID:%03d] groupSyncWrite addparam failed" % scs_id)
        
while 1:
    # Servo (ID1~10) runs at a maximum speed of V=60 * 0.732=43.92rpm and an acceleration of A=50 * 8.7deg/s ^ 2 until it reaches position P1=4095
    for scs_id in IDLIST:
        scs_comm_result, scs_error = packetHandler.RegWritePosEx(scs_id, 3072, 3000, 50)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        if scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))
    packetHandler.RegAction()
    
    time.sleep((3072-1024)/(3000) + 1)#[(P1-P0)/(V*50)] + [(V*50)/(A*100)] + 0.05
    
    # Servo (ID1~10) runs at a maximum speed of V=60 * 0.732=43.92rpm and an acceleration of A=50 * 8.7deg/s ^ 2 until P0=0 position
    for scs_id in IDLIST:
        scs_comm_result, scs_error = packetHandler.RegWritePosEx(scs_id, 1024, 3000, 50)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(scs_comm_result))
        if scs_error != 0:
            print("%s" % packetHandler.getRxPacketError(scs_error))
    packetHandler.RegAction()
    
    time.sleep((3072-1024)/(3000) + 1)#[(P1-P0)/(V*50)] + [(V*50)/(A*100)] + 0.05

# Close port
portHandler.closePort()
