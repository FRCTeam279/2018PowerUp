from wpilib.command import CommandGroup, PrintCommand

import robotmap
from commands.cubeeject import CubeEject
from commands.cuberotatedown import CubeRotateDown
from commands.delay import Delay
from commands.elevatormovetovoltage import ElevatorMoveToVoltage
from commands.navxresetyawangle import NavxResetYawAngle
from commands.tankdriveminencoderdistance import TankDriveMinEncoderDistance
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
        self.addSequential(NavxResetYawAngle())

        self.addParallel(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Rotate part way level"))
        self.addParallel(CubeRotateDown(), timeout=2.25)

        self.addParallel(PrintCommand("CMD Group AutoLoadSwitchToRightFromSide: Raising elevator to 1.21V"))
        self.addParallel(ElevatorMoveToVoltage(1.21), 6)

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToRightFromSide: Drive forward 138 nches"))
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 138,
                                                      p=robotmap.driveLine.pidMedDriveP,
                                                      i=robotmap.driveLine.pidMedDriveI,
                                                      d=robotmap.driveLine.pidMedDriveD,
                                                      tolerance=robotmap.driveLine.pidMedDriveTolerance,
                                                      minSpeed=robotmap.driveLine.pidMedDriveMinSpeed,
                                                      maxSpeed=robotmap.driveLine.pidMedDriveMaxSpeed), timeout=5)


        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToRightFromSide: Delay"))
        self.addSequential(Delay(250))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToRightFromSide: Turn to -90 deg"))
        self.addSequential(TankDriveTurnToHeading(target=-90.0,
                                                  p=robotmap.driveLine.pidMedTurnP,
                                                  i=robotmap.driveLine.pidMedTurnI,
                                                  d=robotmap.driveLine.pidMedTurnD,
                                                  minSpeed=robotmap.driveLine.pidMedTurnMinSpeed,
                                                  tolerance=robotmap.driveLine.pidMedTurnTolerance,
                                                  numSamples=robotmap.driveLine.pidMedTurnSamples,
                                                  steadyRate=robotmap.driveLine.pidMedTurnSteady,
                                                  scaleSpeed=robotmap.driveLine.pidMedTurnScaleSpeed), timeout=4)

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Move In"))
        # TODO - drive to ultrasonic distance ?
        #self.addSequential(TankDriveMinEncoderDistance(target=robotmap.driveLine.inchesPerTick * 20, speed=0.4), timeout=3)
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 30,
                                                      p=robotmap.driveLine.pidSmallDriveP,
                                                      i=robotmap.driveLine.pidSmallDriveI,
                                                      d=robotmap.driveLine.pidSmallDriveD,
                                                      tolerance=robotmap.driveLine.pidSmallDriveTolerance,
                                                      minSpeed=robotmap.driveLine.pidSmallDriveMinSpeed,
                                                      maxSpeed=robotmap.driveLine.pidSmallDriveMaxSpeed), timeout=2.5)

        # self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Rotate Level"))
        # self.addSequential(CubeRotateDown(), timeout=5)

        self.addSequential(PrintCommand("CMD Group AutoLoadScaleToLeft: Cube Eject"))
        self.addSequential(CubeEject(), timeout=3)

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchToRightFromSide: Finished"))

