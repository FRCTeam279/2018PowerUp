# Contains no juice

import wpilib
from commandbased import CommandBasedRobot
from wpilib.command import Scheduler
from wpilib import SmartDashboard
from wpilib.driverstation import DriverStation
from robotpy_ext.common_drivers import navx


# import items in the order they should be initialized to avoid any surprises
import robotmap
import subsystems
import oi
from automanager import AutoManager

autoManager = None


class MyRobot(CommandBasedRobot):

    def robotInit(self):
        print('2018Powerup - robotInit called')
        if robotmap.sensors.hasAHRS:
            try:
                robotmap.sensors.ahrs = navx.AHRS.create_spi()
                # use via robotmap.sensors.ahrs.getAngle()
                print('robotInit: NavX Setup')
            except:
                if not DriverStation.getInstance().isFmsAttached():
                    raise

        #global autoManager
        #autoManager = AutoManager()
        #autoManager.initialize()

        # subsystems must be initialized before things that use them
        subsystems.init()
        oi.init()

    #def autonomousPeriodic(self):
        #global autoManager
        #if len(autoManager.gameData) < 3:
        #    autoManager.gameData = DriverStation.getInstance().getGameSpecificMessage()
        #    print("Auto Periodic: Game Data = {}".format(autoManager.gameData))

        #    if len(autoManager.gameData) > 0:
        #        gameDataNearSwitchSide = autoManager.gameData[0]
        #        gameDataScaleSide = autoManager.gameData[1]
        #        autoCommandToRun = autoManager.getAction(gameDataNearSwitchSide, gameDataScaleSide)
        #        autoCommandToRun.start()
        #        print("Auto Periodic: Started command received from AutoManager")
        #    else:
        #        print("Auto Periodic: Error - gameData was zero length!")
        #super().autonomousPeriodic()

    def teleopPeriodic(self):
        Scheduler.getInstance().run()
        SmartDashboard.putNumber("DL Enc Left", subsystems.driveline.leftEncoder.get())
        SmartDashboard.putNumber("DL Enc Right", subsystems.driveline.rightEncoder.get())

        SmartDashboard.putNumber("EL S1 Top", subsystems.elevator.s1TopLimit())
        SmartDashboard.putNumber("EL S1 Bottom", subsystems.elevator.s1BottomLimit())

        SmartDashboard.putNumber("EL S2 Top", subsystems.elevator.s2TopLimit())
        SmartDashboard.putNumber("EL S2 Bottom", subsystems.elevator.s2BottomLimit())

        SmartDashboard.putNumber("EL Height V", subsystems.elevator.getHeightVoltage())
        SmartDashboard.putNumber("EL Height Inches", subsystems.elevator.getHeightInches())

    def testPeriodic(self):
        wpilib.LiveWindow.run()


if __name__ == '__main__':
    wpilib.run(MyRobot)

