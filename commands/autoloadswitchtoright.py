from wpilib.command import CommandGroup

import robotmap
from commands.delay import Delay
from commands.tankdrivetoencoderdistance import TankDriveToEncoderDistance
from commands.turntoheading import TurnToHeading


class AutoLoadSwitchToRight(CommandGroup):

    def __init__(self):
        super().__init__('AutoLoadSwitchToRight')
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

        # target=0.0, p=0.0, i=0.0, d=0.0, tolerance=0.0, minSpeed=0.0, maxSpeed=0.0, useDashboardValues=False
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.inchesPerTick * 100, p=0.005, d=0.0,
                                                      i=0.0, tolerance=75, minSpeed=0.15, maxSpeed=1.0))
        self.addSequential(Delay(1000))

        # target=0.0, p=0.0, i=0.0, d=0.0, tolerance=0.0, minSpeed=0.0, numSamples=4, steadyRate=2.0,
        # scaleSpeed=0.5, useDashboardValues=False
        self.addSequential(TurnToHeading(target=90.0, p=0.0035, i=0.0000, d=0.0000, minSpeed=0.15, tolerance=3,
                                         numSamples=10, steadyRate=0.5, scaleSpeed=1.0))


        self.addSequential(Delay(250))
        #TODO - drive to ultrasonic distance
        self.addSequential(TankDriveToEncoderDistance(target=robotmap.driveLine.inchesPerTick * 20, p=0.005, d=0.0,
                                                      i=0.0, tolerance=75, minSpeed=0.15, maxSpeed=1.0))

        #self.addSequential(CubeRotateLevel())
        #self.addSequential(Delay(250))
        # self.addSequential(EjectCube())
        # self.addSequential(CubeRaise(8))  #make sure we aren't interfering with switch

