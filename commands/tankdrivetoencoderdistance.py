import time
import math

from wpilib import SmartDashboard
from wpilib.command import Command

import subsystems


class TankDriveToEncoderDistance(Command):
    """
    This command implements a PID loop to drive forward or backward to a target encoder value.

    Notes:
    - The encoder used should increment positively for forward movement
    - Left and right wheel speeds will be set the same
    """
    def __init__(self, target=0.0, p=0.0, i=0.0, d=0.0, tolerance=0.0, minSpeed=0.0, maxSpeed=0.0, useDashboardValues=False):
        super().__init__('TankDriveToEncoderDistance')
        self.requires(subsystems.driveline)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
        self.useSmartDashboardValues = useDashboardValues
        self.target = target
        self.kP = p
        self.kI = i
        self.kD = d
        self.tolerance = tolerance
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed

        self.logCounter = 0

    def initialize(self):
        #print("CMD TankDriveToEncoderDistance initialize called")
        if self.useSmartDashboardValues:
            self.target = SmartDashboard.getNumber("DriveEnc Target", 0.0)

            self.kP = SmartDashboard.getNumber("DriveEnc P", 0.005)
            self.kI = SmartDashboard.getNumber("DriveEnc I", 0.0)
            self.kD = SmartDashboard.getNumber("DriveEnc D", 0.0)

            self.tolerance = SmartDashboard.getNumber("DriveEnc Tolerance", 500.0)
            self.minSpeed = SmartDashboard.getNumber("DriveEnc MinSpeed", 0.0)
            self.maxSpeed = SmartDashboard.getNumber("DriveEnc MaxSpeed", 1.0)

        subsystems.driveline.resetEncoders()
        subsystems.driveline.pidController.setSetpoint(self.target)
        subsystems.driveline.pidController.setAbsoluteTolerance(self.tolerance)
        subsystems.driveline.pidController.setOutputRange(-self.maxSpeed, self.maxSpeed)
        subsystems.driveline.pidController.setPID(self.kP, self.kI, self.kD)

        print("CMD TankDriveToEncoderDistance Starting({}) - target: {}, current: {}, P: {}, I: {}, D: {}, minSpd: {}, maxSpd: {}".format(
            int(round(time.time() * 1000)), self.target, subsystems.driveline.getPIDEncoderCount(),
            self.kP, self.kI, self.kD, self.minSpeed, self.maxSpeed))

    def execute(self):
        if not subsystems.driveline.pidController.isEnabled():
            subsystems.driveline.pidController.enable()

    def isFinished(self):
        count = subsystems.driveline.getPIDEncoderCount()
        res = math.fabs(self.target - count) < self.tolerance
        # self.logCounter += 1
        # if self.logCounter > 50:
        #    print("CMD TankDriveToEncoderDistance isFinished: target={}, encoder={}, tolerance={},
        #       result={}".format(self.target, count, self.tolerance, res))
        if res:
            # print("CMD TankDriveToEncoderDistance isFinished is True")
            return True
        return False

    def end(self):
        print("CMD TankDriveToEncoderDistance Ended({}) - target: {}, current: {}".format(
            int(round(time.time() * 1000)), self.target, subsystems.driveline.getPIDEncoderCount()))
        subsystems.driveline.pidController.reset()
        subsystems.driveline.stop()

    def interrupted(self):
        print("CMD TankDriveToEncoderDistance Interrupted({}) - target: {}, current: {}".format(
            int(round(time.time() * 1000)), self.target, subsystems.driveline.getPIDEncoderCount()))
        subsystems.driveline.pidController.reset()
        subsystems.driveline.stop()

