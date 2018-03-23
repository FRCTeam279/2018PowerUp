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


class AutoLoadSwitchFromMid(CommandGroup):

    def __init__(self, side):

        super().__init__('AutoLoadSwitchFromMid')
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Starting"))
        # TODO - Drive to Ultrasonic Distance
        self.addSequential(NavxResetYawAngle())


        self.addParallel(PrintCommand("CMD Group AutoLoadSwitchFromMid: Cube Rotate part way level"))
        self.addParallel(CubeRotateDown(), timeout=2.25)

        self.addParallel(PrintCommand("CMD Group AutoLoadSwitchFromMid: Raising elevator to 1.21V"))
        self.addParallel(ElevatorMoveToVoltage(1.21), 5)

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Drive Forward off wall"))
        # self.addSequential(TankDriveMinEncoderDistance(target=robotmap.driveLine.inchesPerTick * 12, speed=0.4), timeout=3)
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 16,
                                                      p=robotmap.driveLine.pidSmallDriveP,
                                                      i=robotmap.driveLine.pidSmallDriveI,
                                                      d=robotmap.driveLine.pidSmallDriveD,
                                                      tolerance=robotmap.driveLine.pidSmallDriveTolerance,
                                                      minSpeed=robotmap.driveLine.pidSmallDriveMinSpeed,
                                                      maxSpeed=robotmap.driveLine.pidSmallDriveMaxSpeed), timeout=3)


        if side == 'L':     # angle to left, then right and unload
            self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Turn to -45deg"))
            self.addSequential(
                TankDriveTurnToHeading(target=-45.0,
                                       p=robotmap.driveLine.pidSmallTurnP,
                                       i=robotmap.driveLine.pidSmallTurnI,
                                       d=robotmap.driveLine.pidSmallTurnD,
                                       minSpeed=robotmap.driveLine.pidSmallTurnMinSpeed,
                                       tolerance=robotmap.driveLine.pidSmallTurnTolerance,
                                       numSamples=robotmap.driveLine.pidSmallTurnSamples,
                                       steadyRate=robotmap.driveLine.pidSmallTurnSteady,
                                       scaleSpeed=robotmap.driveLine.pidSmallTurnScaleSpeed), timeout=4)

        else:               # angle to right, then left and unload
            self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Turn to 45deg"))
            self.addSequential(
                TankDriveTurnToHeading(target=45.0,
                                       p=robotmap.driveLine.pidSmallTurnP,
                                       i=robotmap.driveLine.pidSmallTurnI,
                                       d=robotmap.driveLine.pidSmallTurnD,
                                       minSpeed=robotmap.driveLine.pidSmallTurnMinSpeed,
                                       tolerance=robotmap.driveLine.pidSmallTurnTolerance,
                                       numSamples=robotmap.driveLine.pidSmallTurnSamples,
                                       steadyRate=robotmap.driveLine.pidSmallTurnSteady,
                                       scaleSpeed=robotmap.driveLine.pidSmallTurnScaleSpeed), timeout=4)

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Delay"))
        self.addSequential(Delay(100))
        if side == 'L':  # angle to left, then right and unload
            self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Drive Forward Left"))
            # self.addSequential(TankDriveMinEncoderDistance(target=robotmap.driveLine.inchesPerTick * 36, speed=0.4), timeout=4)
            self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 82,
                                                          p=robotmap.driveLine.pidSmallDriveP,
                                                          i=robotmap.driveLine.pidSmallDriveI,
                                                          d=robotmap.driveLine.pidSmallDriveD,
                                                          tolerance=robotmap.driveLine.pidSmallDriveTolerance,
                                                          minSpeed=robotmap.driveLine.pidSmallDriveMinSpeed,
                                                          maxSpeed=robotmap.driveLine.pidSmallDriveMaxSpeed), timeout=3)
        else:
            self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Drive Forward Right"))
            # self.addSequential(TankDriveMinEncoderDistance(target=robotmap.driveLine.inchesPerTick * 36, speed=0.4), timeout=4)
            self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 54,
                                                          p=robotmap.driveLine.pidSmallDriveP,
                                                          i=robotmap.driveLine.pidSmallDriveI,
                                                          d=robotmap.driveLine.pidSmallDriveD,
                                                          tolerance=robotmap.driveLine.pidSmallDriveTolerance,
                                                          minSpeed=robotmap.driveLine.pidSmallDriveMinSpeed,
                                                          maxSpeed=robotmap.driveLine.pidSmallDriveMaxSpeed), timeout=3)


        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Delay"))
        self.addSequential(Delay(100))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Turn to 0deg"))
        self.addSequential(
            TankDriveTurnToHeading(target=0.0,
                                   p=robotmap.driveLine.pidSmallTurnP,
                                   i=robotmap.driveLine.pidSmallTurnI,
                                   d=robotmap.driveLine.pidSmallTurnD,
                                   minSpeed=robotmap.driveLine.pidSmallTurnMinSpeed,
                                   tolerance=robotmap.driveLine.pidSmallTurnTolerance,
                                   numSamples=robotmap.driveLine.pidSmallTurnSamples,
                                   steadyRate=robotmap.driveLine.pidSmallTurnSteady,
                                   scaleSpeed=robotmap.driveLine.pidSmallTurnScaleSpeed), timeout=4)

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Delay"))
        self.addSequential(Delay(100))

        # TODO - try with ultrasonics
        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Drive Forward to wall"))
        if side == 'L':  # angle to left, then right and unload
            # self.addSequential(TankDriveMinEncoderDistance(target=robotmap.driveLine.inchesPerTick * 24, speed=0.4), timeout=3)
            self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 32,
                                                          p=robotmap.driveLine.pidSmallDriveP,
                                                          i=robotmap.driveLine.pidSmallDriveI,
                                                          d=robotmap.driveLine.pidSmallDriveD,
                                                          tolerance=robotmap.driveLine.pidSmallDriveTolerance,
                                                          minSpeed=robotmap.driveLine.pidSmallDriveMinSpeed,
                                                          maxSpeed=robotmap.driveLine.pidSmallDriveMaxSpeed), timeout=3.5)
        else:
            # self.addSequential(TankDriveMinEncoderDistance(target=robotmap.driveLine.inchesPerTick * 24, speed=0.4), timeout=3)
            self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 50,
                                                          p=robotmap.driveLine.pidSmallDriveP,
                                                          i=robotmap.driveLine.pidSmallDriveI,
                                                          d=robotmap.driveLine.pidSmallDriveD,
                                                          tolerance=robotmap.driveLine.pidSmallDriveTolerance,
                                                          minSpeed=robotmap.driveLine.pidSmallDriveMinSpeed,
                                                          maxSpeed=robotmap.driveLine.pidSmallDriveMaxSpeed), timeout=3.5)

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Delay"))
        self.addSequential(Delay(250))

        if side == 'L' or side == 'R':
            # self.addSequential(CubeRotateDown(), timeout=2.5)     -- not needed
            self.addSequential(CubeEject(), timeout=3)
        else:
            self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: invalid value passed for side, will not unload cube"))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Finished"))

