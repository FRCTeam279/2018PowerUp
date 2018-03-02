from wpilib.command import CommandGroup, PrintCommand

import robotmap
from commands.cuberotatedown import CubeRotateDown
from commands.delay import Delay
from commands.elevatormovetovoltage import ElevatorMoveToVoltage
from commands.navxresetyawangle import NavxResetYawAngle
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
        self.addSequential(NavxResetYawAngle())
        # 20' for testing... 20 * 12 = 240
        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToRight: Drive Forward 240 inches"))
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 240,
                                                      p=robotmap.driveLine.pidLargeDriveP,
                                                      i=robotmap.driveLine.pidLargeDriveI,
                                                      d=robotmap.driveLine.pidLargeDriveD,
                                                      tolerance=robotmap.driveLine.pidLargeDriveTolerance,
                                                      minSpeed=robotmap.driveLine.pidLargeDriveMinSpeed,
                                                      maxSpeed=robotmap.driveLine.pidLargeDriveMaxSpeed), timeout=5)

        # TODO - do we need to rotate in a bit?
        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToRight: Rotate in"))

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToRight: Cube Rotate Level"))
        self.addSequential(CubeRotateDown(), timeout=5)

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToRight: Cube Raise"))
        self.addSequential(ElevatorMoveToVoltage(2.79), 8)  #make sure we aren't interfering with switch

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToRight: Move In"))
        # move in a bit more

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToRight: Cube Eject"))
        # self.addSequential(EjectCube())

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToRight: Finished"))

