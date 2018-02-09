import time
import math

from wpilib import SmartDashboard
from wpilib.command import Command

import robotmap
import subsystems


class TurnToHeading(Command):
    """
    This command implements a PID loop to turn the robot to a heading

    target and tolerance are both given in Yaw (-180 to +180)

    It collects samples of the turn rate to determine when turn is finished via measuring how steady the robot is
    Good pid values for Stronghold were 0.05, 0.001, 0.1 (PID)

    ScaleSpeed is how much to reduce the PID output value by to apply to each wheel (eg.. 0.5 will apply half to each
    wheel which is equivilent to the intended output vs no scaling which effectively doubles the turn speed)
    """
    def __init__(self, target=0.0, p=0.0, i=0.0, d=0.0, tolerance=0.0, minSpeed=0.0, numSamples=4, steadyRate=2.0, scaleSpeed=0.5, useDashboardValues=False):
        super().__init__('TurnToHeading')
        self.requires(subsystems.driveline)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
        self.logCounter = 0
        self.useSmartDashboardValues = useDashboardValues
        self.target = target
        self.kP = p
        self.kI = i
        self.kD = d
        self.tolerance = tolerance
        self.minSpeed = minSpeed
        self.scaleSpeed = scaleSpeed

        self.sampleToUpdate = 0     # index for which sample are we updating each pass of execute
        self.ratePasses = 0         # prevent skew when calculating average before we've filled each sample
        self.turnRateSamples = None    # hold the samples
        self.numSamples = numSamples
        self.avgRate = 0.0          # track the current avg turn rate to know when steady
        self.steadyRate = steadyRate


    def initialize(self):
        #print("CMD TurnToHeading initialize called")
        if self.useSmartDashboardValues:
            self.target = SmartDashboard.getNumber("Turn Target", 0.0)
            self.tolerance = SmartDashboard.getNumber("Turn Tolerance", 500.0)
            self.tolerance = SmartDashboard.getNumber("Turn minSpeed", 0.0)
            self.scaleSpeed = SmartDashboard.getNumber("Turn scaleSpeed", 0.5)
            self.kP = SmartDashboard.getNumber("Turn P", 0.05)
            self.kI = SmartDashboard.getNumber("Turn I", 0.001)
            self.kD = SmartDashboard.getNumber("Turn D", 0.01)

        subsystems.driveline.turnPID.minSpeed = self.minSpeed
        subsystems.driveline.turnPID.scaleSpeed = self.scaleSpeed
        subsystems.driveline.pidTurnController.setOutputRange(-1.0, 1.0)
        subsystems.driveline.pidTurnController.setInputRange(-180, 180)
        subsystems.driveline.pidTurnController.setContinuous(True)
        subsystems.driveline.pidTurnController.setPID(self.kP, self.kI, self.kD)
        subsystems.driveline.pidTurnController.setSetpoint(self.target)
        subsystems.driveline.pidTurnController.setAbsoluteTolerance(self.tolerance)


        self.turnRateSamples = [self.steadyRate] * self.numSamples  # biasing to neutral to begin


        print("CMD TurnToHeading Starting({}) - target: {}, current: {}, P: {}, I: {}, D: {}, tolerance: {}, steadyRate: {}, scaleSpeed: {}".format(
            int(round(time.time() * 1000)), self.target, robotmap.sensors.ahrs.getYaw(),
            self.kP, self.kI, self.kD, self.tolerance, self.steadyRate, self.scaleSpeed))

    def execute(self):
        if not subsystems.driveline.pidTurnController.isEnabled():
            subsystems.driveline.pidTurnController.enable()

        if self.numSamples > 0:
            self.turnRateSamples[self.sampleToUpdate] = math.fabs(robotmap.sensors.ahrs.getRate())
            self.sampleToUpdate += 1
            if self.ratePasses <= self.numSamples:
                self.ratePasses += 1
            if self.sampleToUpdate == self.numSamples:
                self.sampleToUpdate = 0


    def isFinished(self):
        if self.numSamples > 0:
            avgRate = sum(self.turnRateSamples) / self.ratePasses

        self.logCounter += 1
        if self.logCounter > 25:
            self.logCounter = 0
            if self.numSamples > 0:
                print("CMD TurnToHeading isFinished - target: {}, current: {}, tolerance: {}, avgRate: {}, steadyRate: {}".format(
                    self.target, robotmap.sensors.ahrs.getYaw(), self.tolerance, avgRate, self.steadyRate))
            else:
                print("CMD TurnToHeading isFinished - target: {}, current: {}, tolerance: {}".format(
                        self.target, robotmap.sensors.ahrs.getYaw(), self.tolerance))

        if self.numSamples > 0:
            if self.useSmartDashboardValues:
                SmartDashboard.putNumber("AvgRateYawDPS", avgRate)
            if avgRate < self.steadyRate:
                if math.fabs(self.target - robotmap.sensors.ahrs.getYaw()) < self.tolerance:
                    # print("CMD TurnToHeading isFinished is True")
                    return True
        else:
            if math.fabs(self.target - robotmap.sensors.ahrs.getYaw()) < self.tolerance:
                # print("CMD TurnToHeading isFinished is True")
                return True
        return False

    def end(self):
        print("CMD TurnToHeading Ended({}) - target: {}, current: {}".format(
            int(round(time.time() * 1000)), self.target, robotmap.sensors.ahrs.getYaw()))
        subsystems.driveline.pidTurnController.reset()
        subsystems.driveline.stop()

    def interrupted(self):
        print("CMD TurnToHeading Interrupted({}) - target: {}, current: {}".format(
            int(round(time.time() * 1000)), self.target, robotmap.sensors.ahrs.getYaw()))
        subsystems.driveline.pidTurnController.reset()
        subsystems.driveline.stop()

