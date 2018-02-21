from wpilib.command import CommandGroup, PrintCommand

import robotmap
from commands.cubeeject import CubeEject
from commands.cuberotatedown import CubeRotateDown
from commands.delay import Delay
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

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Drive Forward 12 inches"))
        # self.addSequential(TankDriveMinEncoderDistance(target=robotmap.driveLine.inchesPerTick * 12, speed=0.4), timeout=3)
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 12,
                                                      p=robotmap.driveLine.pidSmallDriveP,
                                                      i=robotmap.driveLine.pidSmallDriveI,
                                                      d=robotmap.driveLine.pidSmallDriveD,
                                                      tolerance=robotmap.driveLine.pidSmallDriveTolerance,
                                                      minSpeed=robotmap.driveLine.pidSmallDriveMinSpeed,
                                                      maxSpeed=robotmap.driveLine.pidSmallDriveMaxSpeed), timeout=3)

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Delay"))
        self.addSequential(Delay(250))

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
                                       scaleSpeed=robotmap.driveLine.pidSmallTurnScaleSpeed), timeout=5)

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
                                       scaleSpeed=robotmap.driveLine.pidSmallTurnScaleSpeed), timeout=5)

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Delay"))
        self.addSequential(Delay(100))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Drive Forward 36 inches"))
        # self.addSequential(TankDriveMinEncoderDistance(target=robotmap.driveLine.inchesPerTick * 36, speed=0.4), timeout=4)
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 36,
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
        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Drive Forward 24 inches"))
        # self.addSequential(TankDriveMinEncoderDistance(target=robotmap.driveLine.inchesPerTick * 24, speed=0.4), timeout=3)
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 40,
                                                      p=robotmap.driveLine.pidSmallDriveP,
                                                      i=robotmap.driveLine.pidSmallDriveI,
                                                      d=robotmap.driveLine.pidSmallDriveD,
                                                      tolerance=robotmap.driveLine.pidSmallDriveTolerance,
                                                      minSpeed=robotmap.driveLine.pidSmallDriveMinSpeed,
                                                      maxSpeed=robotmap.driveLine.pidSmallDriveMaxSpeed), timeout=3)

        if side == 'L' or side == 'R':
            self.addSequential(CubeRotateDown(), timeout=5)
            self.addSequential(CubeEject(), timeout=3)
        else:
            self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: invalid value passed for side, will not unload cube"))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Finished"))

