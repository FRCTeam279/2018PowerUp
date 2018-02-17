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
config.leftDriverStickNullZone = 0.1
config.rightDriverStickNullZone = 0.1

# Left Joystick
#  unused...

# Right Joystick
config.btnResetYawAngleIndex = 2


# GO Gamepad (Logitech)
config.goGamePadNullZone = 0.03
config.goGamePadStickFilterFactor = 0.2     # for the FilterInput function
config.goGamePadStickScale = 1.5            # for the FilterInput function


config.axisElevator = 1
config.btnElevatorMoveToBottomIndex = 5         # 5 = left bumper
config.btnElevatorMoveToTopIndex = 6            # 6 = right bumper
config.btnElevatorCalibrateHeightIndex = 8      # 8 = start
config.btnCrateLoadIndex = 1                    # 1 = A
config.btnCrateEjectIndex = 4                   # 4 = Y
config.btnCubeRotateUp = 3                      # 3 = X
config.btnCubeRotateDown = 2                    # 2 = X


# ----------------------------------------------------------
# Stick and Button Objects
# ----------------------------------------------------------

leftDriverStick = None
rightDriverStick = None
goGamePad = None
resetYawBtn = None

btnCrateLoad = None
btnCrateEject = None
btnCrateRotateUp = None
btnCrateRotateDown = None

btnElevatorCalibrateHeight = None
btnElevatorMoveToTop = None
btnElevatorMoveToBottom = None


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

    # ----------------------------------------------------------
    # GO Controls
    # ----------------------------------------------------------
    global btnCrateLoad
    global btnCrateEject
    global btnCrateRotateUp
    global btnCrateRotateDown
    btnCrateLoad = JoystickButton(goGamePad, config.btnCrateLoadIndex)
    btnCrateEject = JoystickButton(goGamePad, config.btnCrateEjectIndex)
    btnCrateRotateUp = JoystickButton(goGamePad, config.btnCubeRotateUp)
    btnCrateRotateDown = JoystickButton(goGamePad, config.btnCubeRotateDown)
    btnCrateLoad.whileHeld(CubeGrab())
    btnCrateEject.whileHeld(CubeEject())
    btnCrateRotateUp.whileHeld(CubeRotateUp())
    btnCrateRotateDown.whileHeld(CubeRotateDown())

    if robotmap.devMode:
        global btnElevatorCalibrateHeight
        btnElevatorCalibrateHeight = JoystickButton(goGamePad, config.btnElevatorCalibrateHeightIndex)
        btnElevatorCalibrateHeight.whenPressed(ElevatorCalibrateHeightReading())

        global btnElevatorMoveToBottom
        btnElevatorMoveToBottom = JoystickButton(goGamePad, config.btnElevatorMoveToBottomIndex)
        btnElevatorMoveToBottom.whenPressed(ElevatorMoveToBottom())

        global btnElevatorMoveToTop
        btnElevatorMoveToTop = JoystickButton(goGamePad, config.btnElevatorMoveToTopIndex)
        btnElevatorMoveToTop.whenPressed(ElevatorMoveToTop())


# ----------------------------------------------------------
# Utility Functions
# ----------------------------------------------------------

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

