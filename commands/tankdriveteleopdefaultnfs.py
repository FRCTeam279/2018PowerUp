import math

from wpilib import SmartDashboard
from wpilib.command import Command
import subsystems
import oi
import robotmap


class TankDriveTeleopDefaultNFS(Command):
    """
    This command uses a throttle and turning control scheme in the same manner as Need for Speed
    It's intended to make a robot that uses skid steering feel like a car

    Speed of turning will be adjusted based on throttle, and spining one way then reversing will not happen instantly

    Also, spinning one direction and then taking throttle to full reverse will reverse the direction of turn
    """

    def __init__(self):
        super().__init__('TankDriveTeleopDefaultNFS')
        self.requires(subsystems.driveline)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
        self.targetLeftSpeed = 0.0
        self.targetRightSpeed = 0.0

    def execute(self):
        # subsystems.drive.driveRaw(oi.leftJoystick.getY(), oi.rightJoystick.getY())

        throttle = oi.getRawThrottle()
        turn = oi.getRawTurn()

        if robotmap.nfs.debugTurning:
            SmartDashboard.putNumber("Raw Throttle", throttle)
            SmartDashboard.putNumber("Raw Turn", turn)

        throttle = oi.applyDeadZone(throttle, oi.config.leftDriverStickNullZone)
        turn = oi.applyDeadZone(turn, oi.config.rightDriverStickNullZone)

        if robotmap.nfs.debugTurning:
            SmartDashboard.putNumber("Throttle", throttle)
            SmartDashboard.putNumber("Turn", turn)

        if oi.leftDriverStick.getTrigger():
            throttle *= robotmap.nfs.slowDriveSpeedFactor
            turn *= robotmap.nfs.slowDriveSpeedFactor

        lastLeftSpeed = self.targetLeftSpeed
        lastRightSpeed = self.targetRightSpeed

        self.nfsCalcTrackSpeeds(throttle, turn)
        if robotmap.nfs.debugTurning:
            SmartDashboard.putNumber("targetLeftSpeed", self.targetLeftSpeed)
            SmartDashboard.putNumber("targetRightSpeed", self.targetRightSpeed)


        leftSpeedDiff = lastLeftSpeed - self.targetLeftSpeed
        rightSpeedDiff = lastRightSpeed - self.targetRightSpeed

        if math.fabs(leftSpeedDiff) > robotmap.driveLine.maxSpeedChange:
            if leftSpeedDiff > 0.0:
                leftSpeedDiff = robotmap.driveLine.maxSpeedChange
            if leftSpeedDiff < 0.0:
                leftSpeedDiff = robotmap.driveLine.maxSpeedChange * -1.0

        if math.fabs(rightSpeedDiff) > robotmap.driveLine.maxSpeedChange:
            if rightSpeedDiff > 0.0:
                rightSpeedDiff = robotmap.driveLine.maxSpeedChange
            if rightSpeedDiff < 0.0:
                rightSpeedDiff = robotmap.driveLine.maxSpeedChange * -1.0

        adjustedLeft = lastLeftSpeed - leftSpeedDiff
        adjustedRight = lastRightSpeed - rightSpeedDiff

        if robotmap.nfs.debugTurning:
            SmartDashboard.putNumber("AdjustedLeft", adjustedLeft)
            SmartDashboard.putNumber("AdjustedRight", adjustedRight)

        subsystems.driveline.driveRaw(adjustedLeft, adjustedRight)

    def isFinished(self):
        return False

    def end(self):
        subsystems.driveline.driveRaw(0.0, 0.0)
        self.targetLeftSpeed = 0.0
        self.targetRightSpeed = 0.0
    
    def interrupted(self):
        subsystems.driveline.driveRaw(0.0, 0.0)
        self.targetLeftSpeed = 0.0
        self.targetRightSpeed = 0.0

    def nfsCalcTrackSpeeds(self, rawThrottleSpeed, rawTurnSpeed):
        """
        Throttle will set the base forward or backward speed
        turn will reduce the speed of the slower side

        The amount reduced will be itself reduced based on the throttle
        Example: for full throttle (1.0), and full turn (1.0)
        a reasonably tight arc is found if the fast side is at +1 and the slow side is at +0.3
        So the max reduction would be -2 (to get a +1 value fully reversed to -1.0), and a minimum reduction would be -0.7

        Are there any situations in which the fast side would need to be increased?
        Yes - if the throttle is lower than the turn, the turn reduction to the slow side will be out of kilter with the fast side
                Example - at zero throttle, fast and slow sides should be the inverse of each other

            potential solution:
            if the abs value of slow side is > than fast side, set fast side = slow side

        :param rawThrottleSpeed: Throttle value after filtering joystick input -1.0 to +1.0
        :param rawTurnSpeed: Turn value after filtering -1.0 to +1.0
        """


        # TODO - examine idea of using a minimum speed when throttle is bieng used.  For example,
        # many robots won't start moving until 20-30% power is applied.  Scale from that value rather than zero when
        # applying throttle?

        # TODO - Explor actually setting throttle = turn when abs(fast side) is < abs(slow side) to avoid going
        # in reverse when throttle is low and turning

        leftSpeed = 0.0
        rightSpeed = 0.0

        throttle = math.fabs(rawThrottleSpeed)
        throttleSign = 0.0
        if rawThrottleSpeed > 0.0:
            throttleSign = 1.0
        if rawThrottleSpeed < 0.0:
            throttleSign = -1.0
        if rawThrottleSpeed == 0.0:
            throttleSign = 1.0

        turn = math.fabs(rawTurnSpeed)
        turnSign = 0.0
        if rawTurnSpeed > 0.0:
            turnSign = 1.0
        if rawTurnSpeed < 0.0:
            turnSign = -1.0
        if rawTurnSpeed == 0.0:
            turnSign = 1.0

        # forward + right = clockwise (+1.0)
        # forward + left = counter clockwise (-1.0)
        # back + right = counter clockwise (-1.0)
        # back + left = clockwise (+1.0)
        spinSign = throttleSign * turnSign

        if turn != 0.0:
            fastSide = rawThrottleSpeed
            if oi.leftDriverStick.getTrigger():
                # heavy scaling when driving slow
                turnScale = robotmap.nfs.highTurnScale
            else:
                # light scaling when driving fast
                turnScale = robotmap.nfs.lowTurnScale

            range = 1 - (turnScale * throttle)
            slowSide = throttle - (turn * range)
            slowSide *= throttleSign

            if throttle == 0.0:
                if math.fabs(fastSide) < math.fabs(slowSide):
                    fastSide = slowSide * -1.0

            if spinSign == 1.0:
                leftSpeed = fastSide
                rightSpeed = slowSide

            if spinSign == -1.0:
                leftSpeed = slowSide
                rightSpeed = fastSide
        else:
            # straight ahead
            leftSpeed = rawThrottleSpeed
            rightSpeed = rawThrottleSpeed

        self.targetLeftSpeed = leftSpeed
        self.targetRightSpeed = rightSpeed
