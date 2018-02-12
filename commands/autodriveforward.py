from wpilib.command import CommandGroup

import robotmap
from commands.tankdrivetoencoderdistance import TankDriveToEncoderDistance


class AutoDriveForward(CommandGroup):

    def __init__(self):
        super().__init__('AutoDriveForward')
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

        # target=0.0, p=0.0, i=0.0, d=0.0, tolerance=0.0, minSpeed=0.0, maxSpeed=0.0, useDashboardValues=False
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.inchesPerTick * 60, p=0.005, d=0.0, i=0.0, tolerance=75, minSpeed=0.15, maxSpeed=1.0))





