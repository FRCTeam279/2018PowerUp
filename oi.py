import math
from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton

import robotmap
from commands.cubeeject import CubeEject
from commands.cubegrab import CubeGrab
from commands.cuberotatedown import CubeRotateDown
from commands.cuberotateup import CubeRotateUp
from commands.elevatorcalibrateheightreading import ElevatorCalibrateHeightReading
from commands.elevatormovetobottom import ElevatorMoveToBottom
from commands.elevatormovetotop import ElevatorMoveToTop
from commands.navxresetyawangle import NavxResetYawAngle
from commands.tankdrivereseencoders import TankDriveResetEncoders
from commands.tankdrivetoencoderdistance import TankDriveToEncoderDistance
from commands.tankdriveturntoheading import TankDriveTurnToHeading


class T16000M(Joystick):
    def __init__(self, port):
        super().__init__(port)
        self.port = port
        self.setXChannel(0)
        self.setYChannel(1)
        self.setZChannel(2)
        self.setThrottleChannel(3)
        self.setTwistChannel(2)


# ----------------------------------------------------------
# Config Values
# ----------------------------------------------------------

class ConfigHolder:
    pass


config = ConfigHolder()

# Driver Sticks
config.leftDriverStickNullZone = 0.07
config.rightDriverStickNullZone = 0.07

config.throttleFilterPower = 0.4
config.turnFilterPower = 0.4

# Left Joystickc
config.btnResetEncodersIndex = 2

# Right Joystick
config.btnResetYawAngleIndex = 2


# GO Gamepad (Logitech)
# https://www.desmos.com/calculator/uh8th7djep
config.goGamePadNullZone = 0.03
config.goGamePadStickScale = 0.5            # for the FilterInput function
config.goGamePadStickFilterFactor = 1.0     # for the FilterInput function



config.axisElevator = 1
config.axisClimber = 3
#config.btnElevatorMoveToBottomIndex = 5         # 5 = left bumper
#config.btnElevatorMoveToTopIndex = 6            # 6 = right bumper
#config.btnElevatorCalibrateHeightIndex = 8      # 8 = start
config.btnCrateLoadIndex = 1                    # 1 = A
config.btnCrateEjectIndex = 4                   # 4 = Y
config.btnCubeRotateUp = 3                      # 3 = X
config.btnCubeRotateDown = 2                    # 2 = X

config.axisCubeLoadLeft = 2                     # gamepad trigger
config.axisCubeLoadRight = 3                    # gamepad trigger
config.btnCubeEjectLeft = 5                     #
config.btnCubeEjectRight = 6

# ----------------------------------------------------------
# Stick and Button Objects
# ----------------------------------------------------------

leftDriverStick = None
rightDriverStick = None
goGamePad = None
resetYawBtn = None
btnResetEncoders = None
btnDriveSlow = None

btnCrateLoad = None
btnCrateEject = None
btnCrateRotateUp = None
btnCrateRotateDown = None

btnCubeEjectLeft = None
btnCubeEjectRight = None

# buttons for devmode

# left joystick, buttons 5 - 10
b1 = None
b2 = None
b3 = None
b4 = None
b5 = None
b6 = None

# right joystick, buttons 5 - 10
br1 = None
br2 = None
br3 = None
br4 = None
br5 = None
br6 = None


# ----------------------------------------------------------
# Init
# ----------------------------------------------------------


def init():
    """
    Assign commands to button actions, and publish your joysticks so you
    can read values from them later.
    """

    global leftDriverStick
    global rightDriverStick
    global goGamePad

    try:
        leftDriverStick = T16000M(0)
    except:
        print('OI: Error - Could not instantiate Left Driver Stick on USB port 0!!!')

    try:
        rightDriverStick = T16000M(1)
    except:
        print('OI: Error - Could not instantiate Right Driver Stick on USB port 0!!!')

    try:
        goGamePad = Joystick(2)
    except:
        print('OI: Error - Could not instantiate Game Objective GamePad on USB port 2!!!')

    # ----------------------------------------------------------
    # Driver Controls
    # ----------------------------------------------------------
    global resetYawBtn
    resetYawBtn = JoystickButton(rightDriverStick, config.btnResetYawAngleIndex)
    resetYawBtn.whenPressed(NavxResetYawAngle())

    global btnResetEncoders
    btnResetEncoders = JoystickButton(leftDriverStick, config.btnResetEncodersIndex)
    btnResetEncoders.whenPressed(TankDriveResetEncoders())

    global btnDriveSlow
    btnDriveSlow = JoystickButton(leftDriverStick, 1)

    # ----------------------------------------------------------
    # GO Controls
    # ----------------------------------------------------------
    global btnCrateLoad
    global btnCrateEject
    global btnCrateRotateUp
    global btnCrateRotateDown
    global btnCubeEjectLeft
    global btnCubeEjectRight

    btnCrateLoad = JoystickButton(goGamePad, config.btnCrateLoadIndex)
    btnCrateEject = JoystickButton(goGamePad, config.btnCrateEjectIndex)
    btnCubeEjectLeft = JoystickButton(goGamePad, config.btnCubeEjectLeft)       # will be used in default command
    btnCubeEjectRight = JoystickButton(goGamePad, config.btnCubeEjectLeft)      # will be used in default command
    btnCrateRotateUp = JoystickButton(goGamePad, config.btnCubeRotateUp)
    btnCrateRotateDown = JoystickButton(goGamePad, config.btnCubeRotateDown)
    btnCrateLoad.whileHeld(CubeGrab())
    btnCrateEject.whileHeld(CubeEject())
    btnCrateRotateUp.whileHeld(CubeRotateUp())
    btnCrateRotateDown.whileHeld(CubeRotateDown())

    global b1
    global b2
    global b3
    global b4
    global b5
    global b6

    global br1
    global br2
    global br3
    global br4
    global br5
    global br6

    if robotmap.devMode:
        b1 = JoystickButton(leftDriverStick, 5)
        b2 = JoystickButton(leftDriverStick, 6)
        b3 = JoystickButton(leftDriverStick, 7)
        b4 = JoystickButton(leftDriverStick, 8)
        b5 = JoystickButton(leftDriverStick, 9)
        b6 = JoystickButton(leftDriverStick, 10)

        br1 = JoystickButton(rightDriverStick, 5)
        br2 = JoystickButton(rightDriverStick, 6)
        br3 = JoystickButton(rightDriverStick, 7)
        br4 = JoystickButton(rightDriverStick, 8)
        br5 = JoystickButton(rightDriverStick, 9)
        br6 = JoystickButton(rightDriverStick, 10)

        # forward testing
        b1.whenPressed(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 24, p=0.002, d=0.0, i=0.0, tolerance=15, minSpeed=0.45, maxSpeed=1.0))
        b2.whenPressed(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 36, p=0.0016, d=0.0, i=0.0, tolerance=15, minSpeed=0.45, maxSpeed=1.0))
        b3.whenPressed(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 48, p=0.0014, d=0.0, i=0.0, tolerance=50, minSpeed=0.35, maxSpeed=0.7))
        b4.whenPressed(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 56, p=0.0014, d=0.0, i=0.0, tolerance=50, minSpeed=0.35, maxSpeed=0.7))
        b5.whenPressed(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 100, p=0.0010, d=0.0, i=0.0, tolerance=100, minSpeed=0.35, maxSpeed=0.5))
        b6.whenPressed(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 150, p=0.0010, d=0.0, i=0.0, tolerance=100, minSpeed=0.35, maxSpeed=0.5))

        #b1.whenPressed(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 80, p=0.0010, d=0.0, i=0.0, tolerance=50, minSpeed=0.35, maxSpeed=0.5))
        #b2.whenPressed(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 100, p=0.0010, d=0.0, i=0.0, tolerance=50, minSpeed=0.35, maxSpeed=0.5))
        #b3.whenPressed(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 150, p=0.0010, d=0.0, i=0.0, tolerance=75, minSpeed=0.35, maxSpeed=0.5))
        #b4.whenPressed(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 175, p=0.0010, d=0.0, i=0.0, tolerance=75, minSpeed=0.35, maxSpeed=0.5))
        #b5.whenPressed(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 200, p=0.0010, d=0.0, i=0.0, tolerance=75, minSpeed=0.35, maxSpeed=0.5))
        #b6.whenPressed(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 250, p=0.0010, d=0.0, i=0.0, tolerance=75, minSpeed=0.35, maxSpeed=0.5))

        # turn testing
        # target=0.0, p=0.0, i=0.0, d=0.0, tolerance=0.0, minSpeed=0.0, numSamples=4, steadyRate=2.0, scaleSpeed=0.5,
        br1.whenPressed(TankDriveTurnToHeading(target=22.5,
                                               p=robotmap.driveLine.pidSmallTurnP,
                                               i=robotmap.driveLine.pidSmallTurnI,
                                               d=robotmap.driveLine.pidSmallTurnD,
                                               tolerance=robotmap.driveLine.pidSmallTurnTolerance,
                                               minSpeed=robotmap.driveLine.pidSmallTurnMinSpeed,
                                               numSamples=robotmap.driveLine.pidSmallTurnSamples,
                                               steadyRate=robotmap.driveLine.pidSmallTurnSteady,
                                               scaleSpeed=robotmap.driveLine.pidSmallTurnScaleSpeed))

        br1.whenPressed(TankDriveTurnToHeading(target=45,
                                               p=robotmap.driveLine.pidSmallTurnP,
                                               i=robotmap.driveLine.pidSmallTurnI,
                                               d=robotmap.driveLine.pidSmallTurnD,
                                               tolerance=robotmap.driveLine.pidSmallTurnTolerance,
                                               minSpeed=robotmap.driveLine.pidSmallTurnMinSpeed,
                                               numSamples=robotmap.driveLine.pidSmallTurnSamples,
                                               steadyRate=robotmap.driveLine.pidSmallTurnSteady,
                                               scaleSpeed=robotmap.driveLine.pidSmallTurnScaleSpeed))

        br1.whenPressed(TankDriveTurnToHeading(target=60,
                                               p=robotmap.driveLine.pidMedTurnP,
                                               i=robotmap.driveLine.pidMedTurnI,
                                               d=robotmap.driveLine.pidMedTurnD,
                                               tolerance=robotmap.driveLine.pidMedTurnTolerance,
                                               minSpeed=robotmap.driveLine.pidMedTurnMinSpeed,
                                               numSamples=robotmap.driveLine.pidMedTurnSamples,
                                               steadyRate=robotmap.driveLine.pidMedTurnSteady,
                                               scaleSpeed=robotmap.driveLine.pidMedTurnScaleSpeed))

        br1.whenPressed(TankDriveTurnToHeading(target=90,
                                               p=robotmap.driveLine.pidLargeTurnP,
                                               i=robotmap.driveLine.pidLargeTurnI,
                                               d=robotmap.driveLine.pidLargeTurnD,
                                               tolerance=robotmap.driveLine.pidLargeTurnTolerance,
                                               minSpeed=robotmap.driveLine.pidLargeTurnMinSpeed,
                                               numSamples=robotmap.driveLine.pidLargeTurnSamples,
                                               steadyRate=robotmap.driveLine.pidLargeTurnSteady,
                                               scaleSpeed=robotmap.driveLine.pidLargeTurnScaleSpeed))

        br1.whenPressed(TankDriveTurnToHeading(target=120,
                                               p=robotmap.driveLine.pidLargeTurnP,
                                               i=robotmap.driveLine.pidLargeTurnI,
                                               d=robotmap.driveLine.pidLargeTurnD,
                                               tolerance=robotmap.driveLine.pidLargeTurnTolerance,
                                               minSpeed=robotmap.driveLine.pidLargeTurnMinSpeed,
                                               numSamples=robotmap.driveLine.pidLargeTurnSamples,
                                               steadyRate=robotmap.driveLine.pidLargeTurnSteady,
                                               scaleSpeed=robotmap.driveLine.pidLargeTurnScaleSpeed))

        br1.whenPressed(TankDriveTurnToHeading(target=180,
                                               p=robotmap.driveLine.pidLargeTurnP,
                                               i=robotmap.driveLine.pidLargeTurnI,
                                               d=robotmap.driveLine.pidLargeTurnD,
                                               tolerance=robotmap.driveLine.pidLargeTurnTolerance,
                                               minSpeed=robotmap.driveLine.pidLargeTurnMinSpeed,
                                               numSamples=robotmap.driveLine.pidLargeTurnSamples,
                                               steadyRate=robotmap.driveLine.pidLargeTurnSteady,
                                               scaleSpeed=robotmap.driveLine.pidLargeTurnScaleSpeed))

# ----------------------------------------------------------
# Utility Functions
# ----------------------------------------------------------

# https://www.desmos.com/calculator/yopfm4gkno
# power should be > 0.1 and less than 4 or 5 ish on the outside
#    If power is < 1.0, the curve is a logrithmic curve to give more power closer to center
#    Powers greater than one give a more traditional curve with less sensitivity near center
def filterInputToPower(val, deadZone=0.0, power=2):
    power = math.fabs(power)
    if power < 0.1:
        power = 0.1
    if power > 5:
        power = 5

    sign = 1.0
    if val < 0.0:
        sign = -1.0

    val = math.fabs(val)
    deadZone = math.fabs(deadZone)

    if val < deadZone:
        val = 0.0
    else:
        val = val * ((val - deadZone) / (1 - deadZone))

    output = val ** power
    return output * sign


# View output: https://www.desmos.com/calculator/uh8th7djep
# to keep a straight line, scale = 0, and filterFactor = 1
# Keep filterFactor between 0 and 1
# Scale can go from 0 up, but values over 3-4 have dubious value
# Nice curve for game pad is filterFactor = 0.2, scale=1.5
def filterInput(val, deadZone=0.0, filterFactor=1.0, scale=0.0):
    """
    Filter an input using a curve that makes the stick less sensitive at low input values
    Take into account any dead zone required for values very close to 0.0
    """

    sign = 1.0
    if val < 0.0:
        sign = -1.0

    val = math.fabs(val)
    deadZone = math.fabs(deadZone)

    if val < deadZone:
        val = 0.0
    else:
        val = val * ((val - deadZone) / (1 - deadZone))

    output = val * ((filterFactor * (val**scale)) + ((1 - filterFactor) * val))
    output *= sign
    return output


def applyDeadZone(val, deadZone):
    """
    Apply a dead zone to an input with no other smoothing. Values outsize the dead zone are correctly scaled for 0 to 1.0
    :return:
    The float value of the adjusted intput
    """
    sign = 1.0
    if val < 0.0:
        sign = -1.0

    val = math.fabs(val)
    deadZone = math.fabs(deadZone)

    if val < deadZone:
        val = 0.0
    else:
        val = val * ((val - deadZone) / (1 - deadZone))

    val *= sign
    return val


def getRawThrottle():
    """
    Use the Y Axis of the left stick for throttle.  Value is reversed so that 1.0 is forward (up on a joystick is usually negative input)
    :return:
    The float value of the throttle between -1.0 and 1.0
    """
    val = leftDriverStick.getY()
    if val != 0.0:
        val *= -1.0
    return val


def getRawTurn():
    return rightDriverStick.getX()

