import math
from collections import namedtuple


def calcMagnitude(x, y):
    return math.sqrt((x*x) + (y*y))


def addDegrees(heading, change):
    """
    Calculate a new heading between 0 and 360 degrees
    :param heading: Initial compass heading
    :param change: Degrees to add
    :return: New heading between 0 and 360 degrees
    """
    heading += change
    return heading % 360


def addDegreesYaw(yaw, change):
    """
    Returns a number between -180 and +180
    :param yaw: The initial yaw (-180 to +180)
    :param change:  The degrees to add (positive or negative)
    :return: new yaw value (-180 to 180)
    """
    yaw += change
    yaw %= 360
    if yaw > 180:
        return yaw - 360
    return yaw


def convertYawToDegrees(yaw):
    """
    Converts a yaw which is -180 to 180 to a compass heading between 0 and 360
    Useful in particular for the yaw value that the NavX supplies
    :param yaw: Initial yaw between -180 and 180
    :return: Degrees 0 to 360
    """
    if yaw == 0.0:
        return 0.0
    if yaw > 0.0:
        return 360 % yaw
    if yaw < 0.0:
        yaw += 360
        return 360 % yaw
    return 0.0


def convertDegreesToYaw(degrees):
    # edge case.. if we want the robot to turn left (-degrees) to -180, then we need
    # to track the sign of the input and return -180 in that case
    if degrees < 0.0:
        sign = -1.0
    else:
        sign = 1.0
    degrees %= 360
    if degrees == 180:
        return degrees * sign
    if degrees < 180:
        return degrees
    return degrees - 360


_TurnDirections = namedtuple('TurnDirections', ['left', 'right', 'clockwise', 'counterclockwise'])
turnDirections = _TurnDirections(left=-1.0, right=1.0, clockwise=1.0, counterclockwise=-1.0)


def findTurnDirection(curHeading, targetHeading):
    """
    Find the shortest direction to turn to a new heading.
    Users can compare result with navhelper.turnDirections
    :param curAngle:  current heading 0 to 360
    :param targetAngle:  target heading 0 to 360
    :return: -1.0 for counter clockwise, 1.0 for clockwise
    """
    curHeading %= 360
    targetHeading %= 360
    targetHeading = addDegrees(targetHeading, 360 - curHeading)
    if targetHeading > 180:
        return turnDirections.counterclockwise
    else:
        return turnDirections.clockwise


def getAngleToNewLocation(currentLocation, newLocation):
    """
    Triangulate the angle to a new location using x,y coordinates
    :param currentLocation: tuple of (x, y) for current location.  can use 0, 0 if relative answer is desired
    :param newLocation: tuple of (x, y) for new location
    :return: heading between 0 and 360 to target
    """
    x = currentLocation[0] + newLocation[0]
    y = currentLocation[1] + newLocation[1]
    return math.degrees(math.atan2(x, y))


def getDistanceToNewLocation(currentLocation, newLocation):
    x = currentLocation[0] + newLocation[0]
    y = currentLocation[1] + newLocation[1]
    return math.hypot(x, y)



