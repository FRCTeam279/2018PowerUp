import time
from wpilib.command import Command

import subsystems


class TankDriveMinEncoderDistance(Command):
    """
    This command drives forward/backward at a given speed until it reaches a minimum distance
    No PID loop

    Notes:
    - The encoder used should increment positively for forward movement
    - Left and right wheel speeds will be set the same
    """
    def __init__(self, target=0.0, speed=0.0):
        super().__init__('TankDriveMinEncoderDistance')
        self.requires(subsystems.driveline)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
        self.target = target
        self.speed = speed
        self.logCounter = 0

    def initialize(self):
        subsystems.driveline.resetEncoders()
        print("CMD TankDriveMinEncoderDistance Starting({}) - target: {}, speed {}".format(
            int(round(time.time() * 1000)), self.target, self.speed))

    def execute(self):
        subsystems.driveline.driveRaw(self.speed, self.speed)

    def isFinished(self):
        count = subsystems.driveline.getAvgEncoder()
        return count > self.target

    def end(self):
        print("CMD TankDriveMinEncoderDistance Ended({}) - target: {}, current: {}".format(
            int(round(time.time() * 1000)), self.target, subsystems.driveline.getAvgEncoder()))
        subsystems.driveline.stop()

    def interrupted(self):
        print("CMD TankDriveMinEncoderDistance Interrupted({}) - target: {}, current: {}".format(
            int(round(time.time() * 1000)), self.target, subsystems.driveline.getAvgEncoder()))
        subsystems.driveline.stop()

