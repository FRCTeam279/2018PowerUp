from wpilib.command import CommandGroup, PrintCommand

import robotmap
from commands.cubeeject import CubeEject
from commands.cuberotatedown import CubeRotateDown
from commands.delay import Delay
from commands.tankdriveminencoderdistance import TankDriveMinEncoderDistance
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
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 132,
                                                      p=robotmap.driveLine.pidMedDriveP,
                                                      i=robotmap.driveLine.pidMedDriveI,
                                                      d=robotmap.driveLine.pidMedDriveD,
                                                      tolerance=robotmap.driveLine.pidMedDriveTolerance,
                                                      minSpeed=robotmap.driveLine.pidMedDriveMinSpeed,
                                                      maxSpeed=robotmap.driveLine.pidMedDriveMaxSpeed), timeout=5)

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToLeftFromSide: Delay"))
        self.addSequential(Delay(1000))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToLeftFromSide: Turn to 90 deg"))
        self.addSequential(TankDriveTurnToHeading(target=90.0,
                                                  p=robotmap.driveLine.pidMedTurnP,
                                                  i=robotmap.driveLine.pidMedTurnI,
                                                  d=robotmap.driveLine.pidMedTurnD,
                                                  minSpeed=robotmap.driveLine.pidMedTurnMinSpeed,
                                                  tolerance=robotmap.driveLine.pidMedTurnTolerance,
                                                  numSamples=robotmap.driveLine.pidMedTurnSamples,
                                                  steadyRate=robotmap.driveLine.pidMedTurnSteady,
                                                  scaleSpeed=robotmap.driveLine.pidMedTurnScaleSpeed), timeout=5)

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Move In"))
        # TODO - drive to ultrasonic distance ?
        self.addSequential(TankDriveMinEncoderDistance(target=robotmap.driveLine.inchesPerTick * 20, speed=0.4), timeout=3)

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Rotate Down"))
        self.addSequential(CubeRotateDown(), timeout=5.5)

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Eject"))
        self.addSequential(CubeEject(), timeout=3)

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToLeftFromSide: Finished"))

