from wpilib.command import CommandGroup, PrintCommand

import robotmap
from commands.cuberotatedown import CubeRotateDown
from commands.delay import Delay
from commands.elevatormovetovoltage import ElevatorMoveToVoltage
from commands.navxresetyawangle import NavxResetYawAngle
from commands.tankdrivetoencoderdistance import TankDriveToEncoderDistance
from commands.tankdrivetoencoderdistanceonheading import TankDriveToEncoderDistanceOnHeading
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
        self.addSequential(NavxResetYawAngle())
        # 20' for testing... 20 * 12 = 240
        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Drive Forward 240 inches"))
        self.addSequential(TankDriveToEncoderDistanceOnHeading(target=robotmap.driveLine.ticksPerInch * 240,
                                                      p=robotmap.driveLine.pidLargeDriveP,
                                                      i=robotmap.driveLine.pidLargeDriveI,
                                                      d=robotmap.driveLine.pidLargeDriveD,
                                                      tolerance=robotmap.driveLine.pidLargeDriveTolerance,
                                                      minSpeed=robotmap.driveLine.pidLargeDriveMinSpeed,
                                                      maxSpeed=robotmap.driveLine.pidLargeDriveMaxSpeed,
<<<<<<< Updated upstream
                                                      headingP=0.025), timeout=5)
=======
                                                      headingP=0.03), timeout=5)
>>>>>>> Stashed changes

        # TODO - do we need to rotate in a bit?
        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Rotate in"))

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Rotate Level"))
        self.addSequential(CubeRotateDown(), timeout=2.5)

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Raise"))
        self.addSequential(ElevatorMoveToVoltage(2.79),8)  #make sure we aren't interfering with switch

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Move In"))
        # move in a bit more

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Eject"))
        # self.addSequential(EjectCube())

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Finished"))

