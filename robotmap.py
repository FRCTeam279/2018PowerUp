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
driveLine.invertLeft = True
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
# General Sensors Config
# ----------------------------------------------------------
sensors = ConfigHolder()
sensors.hasAHRS = True


# ----------------------------------------------------------
# Elevator Config (Stages 1 and 2)
# ----------------------------------------------------------
elevator = ConfigHolder()
elevator.s1TopLimitPort = 4                 # digital input
elevator.s1TopLimitNormalClosed = True      # switch is wired to be normally cosed, so will return True when not tripped
elevator.s1BottomLimitPort = 5              # digital input
elevator.s1BottomLimitNormalClosed = True   # switch is wired to be normally cosed, so will return True when not tripped
elevator.s1SpdControllerPort = 3            # pwm
elevator.s1ScaleSpeedUp = 1.0
elevator.s1ScaleSpeedDown = 0.7             # gravity assists
elevator.s1MaxSpeedAtEdgeUp = 0.1           # Maximum speed we should be at when we impact end
elevator.s1MaxSpeedAtEdgeDown = 0.1           # Maximum speed we should be at when we impact end
elevator.s1DistanceToTopToStartSlow = 12    # how far away to start scaling speed down to max
elevator.s1HoldingSpeed = 0.05              # Motor speed required to hold position - used in method #2

elevator.s2TopLimitPort = 6                 # digital input
elevator.s2TopLimitNormalClosed = True      # switch is wired to be normally cosed, so will return True when not tripped
elevator.s2BottomLimitPort = 7              # digital input
elevator.s2BottomLimitNormalClosed = True   # switch is wired to be normally cosed, so will return True when not tripped
elevator.s2SpdControllerPort = 4            # pwm
elevator.s2ScaleSpeedUp = 1.0
elevator.s2ScaleSpeedDown = 0.7             # gravity assists
elevator.s2MaxSpeedAtEdgeUp = 0.1           # Maximum speed we should be at when we impact end
elevator.s2MaxSpeedAtEdgeDown = 0.1           # Maximum speed we should be at when we impact end
elevator.s2DistanceToTopToStartSlow = 12    # how far away to start scaling speed down to max
elevator.s2HoldingSpeed = 0.05              # Motor speed required to hold position - used in method #2

elevator.heightPotPort = 8                  # analog input
elevator.heightVoltsPerInch = 0.0637        # change to calculated once min/max is measured
elevator.heightActualMinVolts = 0.0         # Set via calibration routine
elevator.heightActualMaxVolts = 5.0         # Set via Calibration routine
elevator.heightMaxInches = 74               # Measure and record

elevator.s1AutoMoveUpSpeed = 0.5            # How fast to move when doing a move-to-height command
elevator.s1AutoMoveDownSpeed = 0.3
elevator.s2AutoMoveUpSpeed = 0.5
elevator.s2AutoMoveDownSpeed = 0.3


# ----------------------------------------------------------
# Harvester (Stage 3)
# ----------------------------------------------------------
harvester = ConfigHolder()
harvester.rotationPotPort = 9       # analog input
harvester.relayPort = 0             # relay port


# ----------------------------------------------------------
# Climber
# ----------------------------------------------------------
climber = ConfigHolder()
climber.spdControllerPort = 2       # PWM

# ----------------------------------------------------------
# Ultrasonics
# ----------------------------------------------------------
ultrasonics = ConfigHolder()
ultrasonics.frontRightPingPort = 10
ultrasonics.frontRightEchoPort = 11
ultrasonics.frontLeftPingPort = 12
ultrasonics.frontLeftEchoPort = 13





print("RobotMap module completed load")
