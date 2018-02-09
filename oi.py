import math
from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton

from commands.resetyawangle import ResetYawAngle


class T16000M(Joystick):

    def __init__(self, port):
        super().__init__(port)
        self.port = port
        self.setAxisChannel(Joystick.AxisType.kX, 0)
        self.setAxisChannel(Joystick.AxisType.kY, 1)
        self.setAxisChannel(Joystick.AxisType.kZ, 2)
        self.setAxisChannel(Joystick.AxisType.kThrottle, 3)
        self.setAxisChannel(Joystick.AxisType.kTwist, 2)


leftDriverStick = None
rightDriverStick = None

resetYawBtn = None

class ConfigHolder:
    pass

config = ConfigHolder()
config.leftDriverStickNullZone = 0.05
config.rightDriverStickNullZone = 0.05

# button indexes
config.btnResetYawAngleIndex = 2


def init():
    """
    Assign commands to button actions, and publish your joysticks so you
    can read values from them later.
    """

    global leftDriverStick
    global rightDriverStick

    leftDriverStick = T16000M(0)
    rightDriverStick = T16000M(1)
    resetYawBtn = JoystickButton(rightDriverStick, config.btnResetYawAngleIndex)
    resetYawBtn.whenPressed(ResetYawAngle())


def filterInput(val, deadZone, filterFactor, scale):
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

    output = (filterFactor * (val**scale)) + ((1 - filterFactor) * val)
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

