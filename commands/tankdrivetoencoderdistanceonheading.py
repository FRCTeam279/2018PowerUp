import time
import math

from wpilib import SmartDashboard
from wpilib.command import Command

import robotmap
import subsystems


class TankDriveToEncoderDistanceOnHeading(Command):
    """
    This command implements a PID loop to drive forward or backward to a target encoder value.

    Notes:
    - The encoder used should increment positively for forward movement
    - Left and right wheel speeds will be set the same
    """
    def __init__(self, target=0.0, p=0.0, i=0.0, d=0.0, tolerance=0.0, minSpeed=0.0, maxSpeed=0.0, headingP=0.0):
        super().__init__('TankDriveToEncoderDistanceOnHeading')
        self.requires(subsystems.driveline)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
        self.target = target
        self.kP = p
        self.kI = i
        self.kD = d
        self.tolerance = tolerance
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed
        self.headingP = headingP
        self.heading = 0.0

        self.logCounter = 0

    def initialize(self):

        self.heading = robotmap.sensors.ahrs.getYaw()
        subsystems.driveline.resetEncoders()
        subsystems.driveline.pidControllerIndirect.setSetpoint(self.target)
        subsystems.driveline.pidControllerIndirect.setAbsoluteTolerance(self.tolerance)
        subsystems.driveline.pidControllerIndirect.setOutputRange(-self.maxSpeed, self.maxSpeed)
        subsystems.driveline.pidControllerIndirect.setPID(self.kP, self.kI, self.kD)

        print("CMD TankDriveToEncoderDistanceOhHeading Starting({}) - target: {}, current: {}, P: {}, I: {}, D: {}, minSpd: {}, maxSpd: {}".format(
            int(round(time.time() * 1000)), self.target, subsystems.driveline.getPIDEncoderCount(),
            self.kP, self.kI, self.kD, self.minSpeed, self.maxSpeed))

    def execute(self):
        if not subsystems.driveline.pidControllerIndirect.isEnabled():
            subsystems.driveline.pidControllerIndirect.enable()

        output = subsystems.driveline.tankPIDIndirect.getOutput()
        turnCorrection = (robotmap.sensors.ahrs.getYaw() - self.heading) * self.headingP * -1.0
        if turnCorrection < 0.0:
            left = output - turnCorrection
            right = output + turnCorrection
        else:
            left = output + turnCorrection
            right = output - turnCorrection

        subsystems.driveline.driveRaw(left, right)

    def isFinished(self):
        count = subsystems.driveline.getPIDEncoderCount()
        res = math.fabs(self.target - count) < self.tolerance
        # self.logCounter += 1
        # if self.logCounter > 50:
        #    print("CMD TankDriveToEncoderDistanceOnHeading isFinished: target={}, encoder={}, tolerance={},
        #       result={}".format(self.target, count, self.tolerance, res))
        if res:
            # print("CMD TankDriveToEncoderDistanceOnHeading isFinished is True")
            return True
        return False

    def end(self):
        print("CMD TankDriveToEncoderDistanceOnHeading Ended({}) - target: {}, current: {}".format(
            int(round(time.time() * 1000)), self.target, subsystems.driveline.getPIDEncoderCount()))
        subsystems.driveline.pidControllerIndirect.reset()
        subsystems.driveline.stop()

    def interrupted(self):
        print("CMD TankDriveToEncoderDistanceOhHeading Interrupted({}) - target: {}, current: {}".format(
            int(round(time.time() * 1000)), self.target, subsystems.driveline.getPIDEncoderCount()))
        subsystems.driveline.pidControllerIndirect.reset()
        subsystems.driveline.stop()
