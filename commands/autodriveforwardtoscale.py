from wpilib.command import CommandGroup, PrintCommand

import robotmap
from commands.tankdrivetoencoderdistance import TankDriveToEncoderDistance


class AutoDriveForwardToScale(CommandGroup):

    def __init__(self):
        super().__init__('AutoDriveForwardToScale')
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
        self.addSequential(PrintCommand("CMD Group AutoDriveForwardToScale: Starting"))

        self.addSequential(PrintCommand("CMD Group AutoDriveForwardToScale: Drive Forward 250 inches"))
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 250,
                                                      p=robotmap.driveLine.pidLargeDriveP,
                                                      i=robotmap.driveLine.pidLargeDriveI,
                                                      d=robotmap.driveLine.pidLargeDriveD,
                                                      tolerance=robotmap.driveLine.pidLargeDriveTolerance,
                                                      minSpeed=robotmap.driveLine.pidLargeDriveMinSpeed,
                                                      maxSpeed=robotmap.driveLine.pidLargeDriveMaxSpeed), timeout=5)

        self.addSequential(PrintCommand("CMD Group AutoDriveForwardToScale: Finished"))

