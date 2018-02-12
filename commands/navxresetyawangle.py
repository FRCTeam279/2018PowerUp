from wpilib import DriverStation
from wpilib.command import Command
from robotpy_ext.common_drivers import navx

import robotmap


class NavxResetYawAngle(Command):
    """
    This command resets the Yaw angle for the NavX Gyro
    """

    def __init__(self):
        super().__init__('ResetYawAngle')
        self.setInterruptible(True)
        self.setRunWhenDisabled(True)
        self.resetDone = False

    def initialize(self):
        self.resetDone = False

    def execute(self):
        if not self.resetDone:
            self.resetDone = True
            if robotmap.sensors.hasAHRS:
                try:
                    robotmap.sensors.ahrs.zeroYaw();
                    print('CMD ResetYawAngle: NavX Yaw Zeroed')
                except:
                    print('CMD ResetYawAngle: Exception caught attempted to zero yaw')
                    if not DriverStation.getInstance().isFmsAttached():
                        raise

    def isFinished(self):
        return True

    def end(self):
        pass

    def interrupted(self):
        pass


