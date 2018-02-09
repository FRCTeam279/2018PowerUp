import wpilib
from commandbased import CommandBasedRobot
from robotpy_ext.common_drivers.navx.ahrs import AHRS
import subsystems
import oi


class MyRobot(CommandBasedRobot):

    def robotInit(self):
        print('2018MPowerUp - robotInit called')
        subsystems.init()
        oi.init()


if __name__ == '__main__':
    wpilib.run(MyRobot)

