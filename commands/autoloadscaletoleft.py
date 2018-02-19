from wpilib.command import CommandGroup, PrintCommand

import robotmap
from commands.delay import Delay
from commands.tankdrivetoencoderdistance import TankDriveToEncoderDistance
from commands.tankdriveturntoheading import TankDriveTurnToHeading

# The side of the switch that is ours is on the left, and we will load it from the far left side starting
# position

# drive forward ~25 to be even
# turn to right
# level
# raise
# move in a bit more - slowly
# eject


class AutoLoadScaleToLeft(CommandGroup):

    def __init__(self):
        super().__init__('AutoLoadScaleToLeft')
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Starting"))

        # 20' for testing... 20 * 12 = 240
        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Drive Forward 240 inches"))
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 240,
                                                      p=robotmap.driveLine.pidLargeDriveP,
                                                      i=robotmap.driveLine.pidLargeDriveI,
                                                      d=robotmap.driveLine.pidLargeDriveD,
                                                      tolerance=robotmap.driveLine.pidLargeDriveTolerance,
                                                      minSpeed=robotmap.driveLine.pidLargeDriveMinSpeed,
                                                      maxSpeed=robotmap.driveLine.pidLargeDriveMaxSpeed), timeout=5)

        # TODO - do we need to rotate in a bit?
        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Rotate in"))

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Rotate Level"))
        # self.addSequential(CubeRotateLevel())

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Raise"))
        # self.addSequential(CubeRaise(8))  #make sure we aren't interfering with switch

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Move In"))
        # move in a bit more

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Eject"))
        # self.addSequential(EjectCube())

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Finished"))

