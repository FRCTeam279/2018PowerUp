import math

import wpilib


# ----------------------------------------------------------
# Driveline Subsystem Config
# ----------------------------------------------------------
# flag if we are at competition and want to use development features in the code
# Robot.init() will set this based on FMS being attached
devMode = False


class ConfigHolder:
    """Dummy class to add config parameters too"""
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

#driveLine.driveWheelRadiusInches = 3.1875
#driveLine.driveWheelEncTicks = 360
#driveLine.inchesPerTick = 2 * math.pi * driveLine.driveWheelRadiusInches / driveLine.driveWheelEncTicks
driveLine.inchesPerTick = 0.1536
driveLine.ticksPerInch = 6.5

driveLine.leftEncAPort = 0
driveLine.leftEncBPort = 1
driveLine.leftEncType = wpilib.Encoder.EncodingType.k4X
driveLine.leftEncReverse = True


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

0.02 = 50 times per second (the updated packets to the robot)
"""
driveLine.minTimeFullThrottleChange = 1.5
driveLine.maxSpeedChange = (2 * 0.02) / driveLine.minTimeFullThrottleChange

driveLine.controlStyle = "nfs"


# Small turns <60 deg
# medium turns 60 - 90 deg
# large turns  >90
driveLine.pidSmallTurnP = 0.02
driveLine.pidSmallTurnI = 0.00005
driveLine.pidSmallTurnD = 0.0
driveLine.pidSmallTurnTolerance = 3
driveLine.pidSmallTurnMinSpeed = 0.35
driveLine.pidSmallTurnScaleSpeed = 0.7
driveLine.pidSmallTurnSamples = 5
driveLine.pidSmallTurnSteady = 2

driveLine.pidMedTurnP = 0.02
driveLine.pidMedTurnI = 0.000005
driveLine.pidMedTurnD = 0.0
driveLine.pidMedTurnTolerance = 3
driveLine.pidMedTurnMinSpeed = 0.35
driveLine.pidMedTurnScaleSpeed = 0.7
driveLine.pidMedTurnSamples = 5
driveLine.pidMedTurnSteady = 2

driveLine.pidLargeTurnP = 0.02
driveLine.pidLargeTurnI = 0.000005
driveLine.pidLargeTurnD = 0.0
driveLine.pidLargeTurnTolerance = 3
driveLine.pidLargeTurnMinSpeed = 0.35
driveLine.pidLargeTurnScaleSpeed = 0.6
driveLine.pidLargeTurnSamples = 5
driveLine.pidLargeTurnSteady = 2


# driving forward/backward
# Suggest using TankDriveMinEncoderDistance (NO PID) for distances ~3 feet

# Small = 48 - 100
driveLine.pidSmallDriveP = 0.0015
driveLine.pidSmallDriveI = 0.00005
driveLine.pidSmallDriveD = 0.0
driveLine.pidSmallDriveTolerance = 50
driveLine.pidSmallDriveMinSpeed = 0.35
driveLine.pidSmallDriveMaxSpeed = 0.8

# Medium = 100 - 200
driveLine.pidMedDriveP = 0.001
driveLine.pidMedDriveI = 0.0
driveLine.pidMedDriveD = 0.0
driveLine.pidMedDriveTolerance = 70
driveLine.pidMedDriveMinSpeed = 0.35
driveLine.pidMedDriveMaxSpeed = 0.5

# Large = 200+
driveLine.pidLargeDriveP = 0.001
driveLine.pidLargeDriveI = 0.0
driveLine.pidLargeDriveD = 0.0
driveLine.pidLargeDriveTolerance = 100
driveLine.pidLargeDriveMinSpeed = 0.35
driveLine.pidLargeDriveMaxSpeed = 0.5


# ----------------------------------------------------------
# NFS Driving Config
# ----------------------------------------------------------
nfs = ConfigHolder()
nfs.debugTurning = False
nfs.lowTurnScale = 0.3              # reduce amount of turn when driving at slow speed, 0.3 = 70% reduction
nfs.highTurnScale = 0.2             # reduce amount of turn when driving at high (normal) speed, 0.2 = 80% reduction
nfs.slowDriveSpeedFactor = 0.7      # factor to reduce max speed in slow driving mode. 0.7 = 30% reduction (1.0 * 0.7)


# ----------------------------------------------------------
# General Sensors Config
# ----------------------------------------------------------
sensors = ConfigHolder()
sensors.hasAHRS = True


# ----------------------------------------------------------
# Ultrasonics
# ----------------------------------------------------------
ultrasonics = ConfigHolder()
ultrasonics.frontRightPingPort = 10     # DIO
ultrasonics.frontRightEchoPort = 11
ultrasonics.frontLeftPingPort = 12
ultrasonics.frontLeftEchoPort = 13


# ----------------------------------------------------------
# Elevator Config (Stages 1 and 2)
# ----------------------------------------------------------
elevator = ConfigHolder()

elevator.s1BottomLimitPort = 4              # digital input
elevator.s1BottomLimitNormalClosed = False  # switch is wired to be normally cosed, so will return True when not tripped
elevator.s1TopLimitPort = 5                 # digital input
elevator.s1TopLimitNormalClosed = False     # switch is wired to be normally cosed, so will return True when not tripped
elevator.s1SpdControllerPort = 3            # pwm
elevator.s1SpdControllerReverse = False

elevator.s1ScaleSpeedUp = 1.0               # how much to adjust desired speed by (1 = no change - 100%)
elevator.s1ScaleSpeedDown = 1.0             # gravity assists
elevator.s1MaxSpeedAtEdgeUp = 0.1           # Maximum speed we should be at when we impact end
elevator.s1MaxSpeedAtEdgeDown = 0.1           # Maximum speed we should be at when we impact end
elevator.s1DistanceToTopToStartSlow = 12    # how far away to start scaling speed down to max
elevator.s1HoldingSpeed = 0.0

elevator.s2BottomLimitPort = 6              # digital input
elevator.s2BottomLimitNormalClosed = False  # switch is wired to be normally cosed, so will return True when not tripped
elevator.s2TopLimitPort = 7                 # digital input
elevator.s2TopLimitNormalClosed = False     # switch is wired to be normally cosed, so will return True when not tripped
elevator.s2SpdControllerPort = 4            # pwm
elevator.s2SpdControllerReverse = False

elevator.s2ScaleSpeedUp = 1.0               # how much to adjust desired speed by (1 = no change - 100%)
elevator.s2ScaleSpeedDown = 0.7             # gravity assists
elevator.s2MaxSpeedAtEdgeUp = 0.1           # Maximum speed we should be at when we impact end
elevator.s2MaxSpeedAtEdgeDown = 0.1         # Maximum speed we should be at when we impact end
elevator.s2DistanceToTopToStartSlow = 12    # how far away to start scaling speed down to max
elevator.s2HoldingSpeed = 0.0              # Motor speed required to hold position - used in method #2

elevator.heightPotPort = 0                  # analog input
elevator.heightVoltsPerInch = 0.0637        # change to calculated once min/max is measured
elevator.heightActualMinVolts = 0.0         # Set via calibration routine
elevator.heightActualMaxVolts = 5.0         # Set via Calibration routine
elevator.heightMaxInches = 74               # Measure and record

elevator.s1AutoMoveUpSpeed = 0.2            # How fast to move when doing a move-to-height command
elevator.s1AutoMoveDownSpeed = 0.15
elevator.s2AutoMoveUpSpeed = 0.3
elevator.s2AutoMoveDownSpeed = 0.25


# ----------------------------------------------------------
# Harvester (Stage 3)
# ----------------------------------------------------------
harvester = ConfigHolder()
harvester.rotationSpdPort = 5               # Rotation the cubinator3000 up and down
harvester.rotationSpdReverse = False        # do we need to invert the speed controller
harvester.rotationPotPort = 9               # analog input
harvester.relayPort = 0                     # relay port

harvester.rotateUpSpeed = 0.3
harvester.rotateDownSpeed = 0.2


# ----------------------------------------------------------
# Climber
# ----------------------------------------------------------
climber = ConfigHolder()
climber.spdControllerPort = 2       # PWM
climber.spdControllerReverse = False

print("RobotMap module completed load")

