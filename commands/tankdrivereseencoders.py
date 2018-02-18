import time
import math

from wpilib import SmartDashboard
from wpilib.command import Command

import robotmap
import subsystems


class TankDriveResetEncoders(Command):

    def __init__(self):
        super().__init__('TankDriveTurnToHeading')
        self.requires(subsystems.driveline)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

    def execute(self):
        subsystems.driveline.resetEncoders()
        print("CMD TankDriveResetEncoders: Reset Completed")

    def isFinished(self):
       return True

