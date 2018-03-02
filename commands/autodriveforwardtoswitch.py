from wpilib.command import CommandGroup, PrintCommand

import robotmap
from commands.navxresetyawangle import NavxResetYawAngle
from commands.tankdrivetoencoderdistance import TankDriveToEncoderDistance


class AutoDriveForwardToSwitch(CommandGroup):

    def __init__(self):
        super().__init__('AutoDriveForwardToSwitch')
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
        self.addSequential(PrintCommand("CMD Group AutoDriveForwardToSwitch: Starting"))
        self.addSequential(NavxResetYawAngle())
        self.addSequential(PrintCommand("CMD Group AutoDriveForwardToSwitch: Drive Forward 132 inches"))
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 132,
                                                      p=robotmap.driveLine.pidMedDriveP,
                                                      i=robotmap.driveLine.pidMedDriveI,
                                                      d=robotmap.driveLine.pidMedDriveD,
                                                      tolerance=robotmap.driveLine.pidMedDriveTolerance,
                                                      minSpeed=robotmap.driveLine.pidMedDriveMinSpeed,
                                                      maxSpeed=robotmap.driveLine.pidMedDriveMaxSpeed), timeout=5)

        self.addSequential(PrintCommand("CMD Group AutoDriveForwardToSwitch: Finished"))

