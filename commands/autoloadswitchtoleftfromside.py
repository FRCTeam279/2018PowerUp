from wpilib.command import CommandGroup, PrintCommand

import robotmap
from commands.delay import Delay
from commands.tankdrivetoencoderdistance import TankDriveToEncoderDistance
from commands.tankdriveturntoheading import TankDriveTurnToHeading

# The side of the switch that is ours is on the left, and we will load it from the far left side starting
# position

# drive forward 132" (11') with timeout
# turn right with timeout
# raise cube
# drive forward with timeout
# level cube
# eject cube


class AutoLoadSwitchToLeftFromSide(CommandGroup):

    def __init__(self):
        super().__init__('AutoLoadSwitchToLeftFromSide')
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToLeftFromSide: Starting"))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToLeftFromSide: Drive forward 132 inches"))
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 132, p=0.005, d=0.0,
                                                      i=0.0, tolerance=75, minSpeed=0.15, maxSpeed=1.0))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToLeftFromSide: Delay"))
        self.addSequential(Delay(1000))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToLeftFromSide: Turn to 90 deg"))
        self.addSequential(TankDriveTurnToHeading(target=90.0, p=0.0035, i=0.0000, d=0.0000, minSpeed=0.15, tolerance=3,
                                                  numSamples=10, steadyRate=0.5, scaleSpeed=1.0))

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Raise"))
        # self.addSequential(CubeRaise(8))  #make sure we aren't interfering with switch

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Move In"))
        # TODO - drive to ultrasonic distance ?
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 20, p=0.005, d=0.0,
                                                      i=0.0, tolerance=75, minSpeed=0.15, maxSpeed=1.0))

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Rotate Level"))
        # self.addSequential(CubeRotateLevel())

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Eject"))
        # self.addSequential(EjectCube())


        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToLeftFromSide: Finished"))

