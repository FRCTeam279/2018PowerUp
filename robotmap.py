import math

import wpilib


class ConfigHolder:
    '''''Dummy class to add config parameters too'''
    pass


# ----------------------------------------------------------
# Driveline Subsystem Config
# ----------------------------------------------------------
driveLine = ConfigHolder()
driveLine.leftMotorPort = 0
driveLine.rightMotorPort = 1
driveLine.invertLeft = False
driveLine.invertRight = False
driveLine.speedControllerType = "TALON"

driveLine.driveWheelRadiusInches = 3.1875
driveLine.driveWheelEncTicks = 360
driveLine.inchesPerTick = 2 * math.pi * driveLine.driveWheelRadiusInches / driveLine.driveWheelEncTicks

driveLine.leftEncAPort = 0
driveLine.leftEncBPort = 1
driveLine.leftEncType = wpilib.Encoder.EncodingType.k4X
driveLine.leftEncReverse = False


driveLine.rightEncAPort = 2
driveLine.rightEncBPort = 3
driveLine.rightEncType = wpilib.Encoder.EncodingType.k4X
driveLine.rightEncReverse = False

"""
minTimeFullThrottleChange
The minimum amount of time that the tank drive will allow the motors to switch from -1.0 to +1.0
Example: a value of 1 means that it will take 1 sec for the speed controllers to be updated from -1.0 to +1.0

The maximum speed controller change per periodic call is thus 
maxThrottleChange = totalThrottleRange (2) * callSpeed (0.02sec) / time (minTimeFullThrottleChange)

0.02 = 50 times per second (the updated packets to the robot
"""
driveLine.minTimeFullThrottleChange = 1.5
driveLine.maxSpeedChange = (2 * 0.02) / driveLine.minTimeFullThrottleChange

driveLine.controlStyle = "nfs"


# ----------------------------------------------------------
# NFS Driving Config
# ----------------------------------------------------------
nfs = ConfigHolder()
nfs.debugTurning = True
nfs.lowTurnScale = 0.3
nfs.highTurnScale = 0.2
nfs.slowDriveSpeedFactor = 0.7


# ----------------------------------------------------------
# Sensors Config
# ----------------------------------------------------------
sensors = ConfigHolder()
sensors.hasAHRS = True

print("RobotMap module completed load")
