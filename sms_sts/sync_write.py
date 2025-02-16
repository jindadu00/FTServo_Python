#!/usr/bin/env python
#
# *********     Sync Write Example      *********
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


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler('COM3')# ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

# Initialize PacketHandler instance
# Get methods and members of Protocol
packetHandler = sms_sts(portHandler)

IDLIST = [1, 2, 3]

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
    for scs_id in IDLIST:
        # Add servo(id)#1~10 goal position\moving speed\moving accc value to the Syncwrite parameter storage
        # Servo (ID1~10) runs at a maximum speed of V=60 * 0.732=43.92rpm and an acceleration of A=50 * 8.7deg/s ^ 2 until it reaches position P1=4095
        scs_addparam_result = packetHandler.SyncWritePosEx(scs_id, 3072-256, 0, 0)
        if scs_addparam_result != True:
            print("[ID:%03d] groupSyncWrite addparam failed" % scs_id)

    # Syncwrite goal position
    scs_comm_result = packetHandler.groupSyncWrite.txPacket()
    if scs_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(scs_comm_result))

    # Clear syncwrite parameter storage
    packetHandler.groupSyncWrite.clearParam()

    time.sleep(3)

    for scs_id in IDLIST:
        # Add servo#1~10 goal position\moving speed\moving accc value to the Syncwrite parameter storage
        # acceleration unit 100/s^2
        scs_addparam_result = packetHandler.SyncWritePosEx(scs_id, 1024+256, 0, 0)
        if scs_addparam_result != True:
            print("[ID:%03d] groupSyncWrite addparam failed" % scs_id)

    # Syncwrite goal position
    scs_comm_result = packetHandler.groupSyncWrite.txPacket()
    if scs_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(scs_comm_result))
    
    # Clear syncwrite parameter storage
    packetHandler.groupSyncWrite.clearParam()
    
    time.sleep(3)

# Close port
portHandler.closePort()
