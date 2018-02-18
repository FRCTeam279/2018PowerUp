from wpilib.command import CommandGroup, PrintCommand

import robotmap
from commands.delay import Delay
from commands.tankdrivetoencoderdistance import TankDriveToEncoderDistance
from commands.tankdriveturntoheading import TankDriveTurnToHeading


class AutoLoadSwitchFromMid(CommandGroup):

    def __init__(self, side):

        super().__init__('AutoLoadSwitchFromMid')
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Starting"))
        # TODO - Drive to Ultrasonic Distance

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Drive Forward 1'"))
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.inchesPerTick * 12, p=0.005, d=0.0,
                                                      i=0.0, tolerance=75, minSpeed=0.15, maxSpeed=1.0))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Delay"))
        self.addSequential(Delay(250))

        if side == 'L':     # angle to left, then right and unload
            self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Turn to -45deg"))
            self.addSequential(
                TankDriveTurnToHeading(target=-45.0, p=0.0035, i=0.0000, d=0.0000, minSpeed=0.15, tolerance=3,
                                       numSamples=10, steadyRate=0.5, scaleSpeed=1.0))
        else:               # angle to right, then left and unload
            self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Turn to 45deg"))
            self.addSequential(
                TankDriveTurnToHeading(target=-45.0, p=0.0035, i=0.0000, d=0.0000, minSpeed=0.15, tolerance=3,
                                       numSamples=10, steadyRate=0.5, scaleSpeed=1.0))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Delay"))
        self.addSequential(Delay(250))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Drive Forward 3'"))
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 12, p=0.005, d=0.0,
                                                      i=0.0, tolerance=75, minSpeed=0.15, maxSpeed=1.0))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Delay"))
        self.addSequential(Delay(250))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Turn to 0deg"))
        self.addSequential(
            TankDriveTurnToHeading(target=0.0, p=0.0035, i=0.0000, d=0.0000, minSpeed=0.15, tolerance=3,
                                   numSamples=10, steadyRate=0.5, scaleSpeed=1.0))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Delay"))
        self.addSequential(Delay(250))

        # TODO - try with ultrasonics
        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Drive Forward 2'"))
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.ticksPerInch * 24, p=0.005, d=0.0,
                                                      i=0.0, tolerance=75, minSpeed=0.15, maxSpeed=1.0))

        if side == 'L' or side == 'R':
            pass
            # self.addSequential(CubeRaise(12))     #make sure we aren't interfering with switch
            # self.addSequential(Delay(250))
            # self.addSequential(CubeRotateLevel())
            # self.addSequential(Delay(250))
            # self.addSequential(EjectCube())
        else:
            self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: invalid value passed for side, will not unload cube"))

        self.addSequential(PrintCommand("CMD Group AutoLoadSwitchFromMid: Finished"))

