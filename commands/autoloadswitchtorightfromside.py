from wpilib.command import CommandGroup, PrintCommand

import robotmap
from commands.delay import Delay
from commands.tankdrivetoencoderdistance import TankDriveToEncoderDistance
from commands.tankdriveturntoheading import TankDriveTurnToHeading

# The side of the switch that is ours is on the right, and we will load it from the far right side starting
# position

# drive forward 132" (11') with timeout
# turn left with timeout
# raise cube
# drive forward with timeout
# level cube
# eject cube


class AutoLoadSwitchToRightFromSide(CommandGroup):

    def __init__(self):
        super().__init__('AutoLoadSwitchToRightFromSide')
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToRightFromSide: Starting"))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToRightFromSide: Drive forward 132 inches"))
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 132,
                                                      p=robotmap.driveLine.pidMedDriveP,
                                                      i=robotmap.driveLine.pidMedDriveI,
                                                      d=robotmap.driveLine.pidMedDriveD,
                                                      tolerance=robotmap.driveLine.pidMedDriveTolerance,
                                                      minSpeed=robotmap.driveLine.pidMedDriveMinSpeed,
                                                      maxSpeed=robotmap.driveLine.pidMedDriveMaxSpeed), timeout=5)

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToRightFromSide: Delay"))
        self.addSequential(Delay(1000))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToRightFromSide: Turn to -90 deg"))
        self.addSequential(TankDriveTurnToHeading(target=-90.0,
                                                  p=robotmap.driveLine.pidMedTurnP,
                                                  i=robotmap.driveLine.pidMedTurnI,
                                                  d=robotmap.driveLine.pidMedTurnD,
                                                  minSpeed=robotmap.driveLine.pidMedTurnMinSpeed,
                                                  tolerance=robotmap.driveLine.pidMedTurnTolerance,
                                                  numSamples=robotmap.driveLine.pidMedTurnSamples,
                                                  steadyRate=robotmap.driveLine.pidMedTurnSteady,
                                                  scaleSpeed=robotmap.driveLine.pidMedTurnScaleSpeed), timeout=5)

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Raise"))
        # self.addSequential(CubeRaise(8))  #make sure we aren't interfering with switch

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Move In"))
        # TODO - drive to ultrasonic distance ?
        self.addSequential(TankDriveMinEncoderDistance(target=robotmap.driveLine.inchesPerTick * 20, speed=0.4), timeout=3)

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Rotate Level"))
        # self.addSequential(CubeRotateLevel())

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Eject"))
        # self.addSequential(EjectCube())

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToRightFromSide: Finished"))

