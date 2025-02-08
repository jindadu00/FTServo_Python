#!/usr/bin/env python
#
# *********     Gen Write Example      *********
#
#
# Available SCServo model on this example : All models using Protocol SCS
# This example is tested with a SCServo(SCS), and an URT
#

import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from scservo_sdk import *                      # Uses FTServo SDK library

SCS_ID = 1
def read(scs_goal_position):
    while 1:
        # Read the current position of servo(ID1)
        scs_present_position, scs_present_speed, scs_comm_result, scs_error = packetHandler.ReadPosSpeed(SCS_ID)

        if scs_comm_result != COMM_SUCCESS:
            print(packetHandler.getTxRxResult(scs_comm_result))
        else:
            print("[ID:%03d] GoalPos:%d PresPos:%d PresSpd:%d" % (SCS_ID, scs_goal_position, scs_present_position, scs_present_speed))
        if scs_error != 0:
            print(packetHandler.getRxPacketError(scs_error))

        # Read moving status of servo(ID1)
        moving, scs_comm_result, scs_error = packetHandler.ReadMoving(1)
        if scs_comm_result != COMM_SUCCESS:
            print(packetHandler.getTxRxResult(scs_comm_result))

        if moving==0:
            break
    return

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler('/dev/ttyUSB0')# ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

# Initialize PacketHandler instance
# Get methods and members of Protocol
packetHandler = scscl(portHandler)
    
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

while 1:
    # Servo (ID1) runs at a maximum speed of V=1500*0.059=88.5rpm until it reaches position P1=1000
    scs_comm_result, scs_error = packetHandler.WritePos(1, 2048, 0, 1000)
    if scs_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(scs_comm_result))
    if scs_error != 0:
        print("%s" % packetHandler.getRxPacketError(scs_error))
    # time.sleep(2)
    read(2048)# Read the status of the servo (ID1) until the servo runs to the target position

    # Servo (ID1) runs at a maximum speed of V=1500*0.059=88.5rpm until it reaches position P0=20
    scs_comm_result, scs_error = packetHandler.WritePos(1, 1024, 0, 1000)
    if scs_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(scs_comm_result))
    if scs_error != 0:
        print("%s" % packetHandler.getRxPacketError(scs_error))
    # time.sleep(2)
    read(1024)# Read the status of the servo (ID1) until the servo runs to the target position
# Close port
portHandler.closePort()
