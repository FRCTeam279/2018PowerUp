from wpilib.command import CommandGroup

import robotmap
from commands.delay import Delay
from commands.tankdrivetoencoderdistance import TankDriveToEncoderDistance
from commands.tankdriveturntoheading import TankDriveTurnToHeading


class AutoLoadSwitchAhead(CommandGroup):

    def __init__(self):
        super().__init__('AutoLoadSwitchAhead')
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

        # TODO - Drive to Ultrasonic Distance
        # target=0.0, p=0.0, i=0.0, d=0.0, tolerance=0.0, minSpeed=0.0, maxSpeed=0.0, useDashboardValues=False
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.inchesPerTick * 100, p=0.005, d=0.0,
                                                      i=0.0, tolerance=75, minSpeed=0.15, maxSpeed=1.0))

        self.addSequential(Delay(250))

        #self.addSequential(CubeRotateLevel())
        #self.addSequential(Delay(250))
        # self.addSequential(EjectCube())
        # self.addSequential(CubeRaise(8))  #make sure we aren't interfering with switch
