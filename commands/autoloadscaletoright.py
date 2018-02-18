from wpilib.command import CommandGroup, PrintCommand

import robotmap
from commands.delay import Delay
from commands.tankdrivetoencoderdistance import TankDriveToEncoderDistance
from commands.tankdriveturntoheading import TankDriveTurnToHeading

# The side of the switch that is ours is on the left, and we will load it from the far left side starting
# position

# drive forward ~25 to be even
# turn to left
# level
# raise
# move in a bit more - slowly
# eject


class AutoLoadScaleToRight(CommandGroup):

    def __init__(self):
        super().__init__('AutoLoadScaleToRight')
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToRight: Starting"))

        # 20' for testing... 20 * 12 = 240
        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToRight: Drive Forward 240 inches"))
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 240, p=0.005, d=0.0,
                                                      i=0.0, tolerance=75, minSpeed=0.15, maxSpeed=1.0))

        # TODO - do we need to rotate in a bit?
        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToRight: Rotate in"))

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToRight: Cube Rotate Level"))
        # self.addSequential(CubeRotateLevel())

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToRight: Cube Raise"))
        # self.addSequential(CubeRaise(8))  #make sure we aren't interfering with switch

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToRight: Move In"))
        # move in a bit more

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToRight: Cube Eject"))
        # self.addSequential(EjectCube())

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToRight: Finished"))

