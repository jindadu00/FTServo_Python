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
from scservo_sdk import *  # Uses FTServo SDK library


# Define COM port for each group of servos
COM_PORTS = {
    1: 'COM6',  # COM6 controls ID 1, 2, 3, 7, 8, 9
    2: 'COM5'   # COM5 controls ID 4, 5, 6
}

# Define servo IDs for each COM port
IDLIST_COM6 = [1, 2, 3, 7, 8, 9]
IDLIST_COM5 = [4, 5, 6]


# Function to initialize the port and packet handler
def initialize_port_handler(com_port):
    portHandler = PortHandler(com_port)
    if portHandler.openPort():
        print(f"Succeeded to open the port {com_port}")
    else:
        print(f"Failed to open the port {com_port}")
        quit()
    
    if not portHandler.setBaudRate(1000000):
        print(f"Failed to change the baudrate for {com_port}")
        quit()
    
    packetHandler = sms_sts(portHandler)
    return portHandler, packetHandler


# Initialize ports for COM5 and COM6
portHandler_COM6, packetHandler_COM6 = initialize_port_handler(COM_PORTS[1])
portHandler_COM5, packetHandler_COM5 = initialize_port_handler(COM_PORTS[2])

# Initialize servos for both COM ports
for scs_id in IDLIST_COM6:
    scs_comm_result, scs_error = packetHandler_COM6.ServoMode(scs_id)
    if scs_comm_result != True:
        print(f"[ID:{scs_id:03d}] groupSyncWrite addparam failed on COM6")

for scs_id in IDLIST_COM5:
    scs_comm_result, scs_error = packetHandler_COM5.ServoMode(scs_id)
    if scs_comm_result != True:
        print(f"[ID:{scs_id:03d}] groupSyncWrite addparam failed on COM5")


# SyncWrite in a loop for both COM ports
while 1:
    # First, set parameters for servos on COM6
    for scs_id in IDLIST_COM6:
        scs_addparam_result = packetHandler_COM6.SyncWritePosEx(scs_id, 2048 - 128, 0, 0)
        if scs_addparam_result != True:
            print(f"[ID:{scs_id:03d}] groupSyncWrite addparam failed on COM6")

    # Syncwrite goal position for COM6 servos
    scs_comm_result = packetHandler_COM6.groupSyncWrite.txPacket()
    if scs_comm_result != COMM_SUCCESS:
        print(f"{packetHandler_COM6.getTxRxResult(scs_comm_result)}")

    # Now, set parameters for servos on COM5
    for scs_id in IDLIST_COM5:
        scs_addparam_result = packetHandler_COM5.SyncWritePosEx(scs_id, 2048 - 128, 0, 0)
        if scs_addparam_result != True:
            print(f"[ID:{scs_id:03d}] groupSyncWrite addparam failed on COM5")

    # Syncwrite goal position for COM5 servos
    scs_comm_result = packetHandler_COM5.groupSyncWrite.txPacket()
    if scs_comm_result != COMM_SUCCESS:
        print(f"{packetHandler_COM5.getTxRxResult(scs_comm_result)}")

    packetHandler_COM6.groupSyncWrite.clearParam()
    packetHandler_COM5.groupSyncWrite.clearParam()
    time.sleep(2)

    # Repeat the above steps with different positions (example for 1024 + 256)
    for scs_id in IDLIST_COM6:
        scs_addparam_result = packetHandler_COM6.SyncWritePosEx(scs_id, 2048 + 128, 0, 0)
        if scs_addparam_result != True:
            print(f"[ID:{scs_id:03d}] groupSyncWrite addparam failed on COM6")

    scs_comm_result = packetHandler_COM6.groupSyncWrite.txPacket()
    if scs_comm_result != COMM_SUCCESS:
        print(f"{packetHandler_COM6.getTxRxResult(scs_comm_result)}")


    for scs_id in IDLIST_COM5:
        scs_addparam_result = packetHandler_COM5.SyncWritePosEx(scs_id, 2048 + 128, 0, 0)
        if scs_addparam_result != True:
            print(f"[ID:{scs_id:03d}] groupSyncWrite addparam failed on COM5")

    scs_comm_result = packetHandler_COM5.groupSyncWrite.txPacket()
    if scs_comm_result != COMM_SUCCESS:
        print(f"{packetHandler_COM5.getTxRxResult(scs_comm_result)}")

    packetHandler_COM6.groupSyncWrite.clearParam()
    packetHandler_COM5.groupSyncWrite.clearParam()

    time.sleep(2)

# Close ports
portHandler_COM6.closePort()
portHandler_COM5.closePort()
