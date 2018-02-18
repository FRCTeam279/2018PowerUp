from wpilib.command import CommandGroup, PrintCommand

import robotmap
from commands.tankdrivetoencoderdistance import TankDriveToEncoderDistance


class AutoDriveForwardToScale(CommandGroup):

    def __init__(self):
        super().__init__('AutoDriveForwardToScale')
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
        self.addSequential(PrintCommand("CMD Group AutoDriveForwardToScale: Starting"))

        self.addSequential(PrintCommand("CMD Group AutoDriveForwardToScale: Drive Forward 200 inches"))
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 200, p=0.005, d=0.0,
                                                      i=0.0, tolerance=75, minSpeed=0.15, maxSpeed=1.0), timeout=5)

        self.addSequential(PrintCommand("CMD Group AutoDriveForwardToScale: Finished"))




