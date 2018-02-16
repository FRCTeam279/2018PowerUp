import wpilib
from wpilib.ultrasonic import Ultrasonic
from wpilib.command.subsystem import Subsystem
import subsystems
import robotmap
from commands.ultrasonicprintrange import UltrasonicPrintRange


class Ultrasonics(Subsystem):

    def __init__(self):
        print('Ultrasonics: init called')
        super().__init__('Ultrasonics')
        self.debug = False
        self.logPrefix = "Ultrasonics: "
        self.frontLeft = Ultrasonic(robotmap.ultrasonics.frontLeftPingPort, robotmap.ultrasonics.frontLeftEchoPort)
        self.frontRight = Ultrasonic(robotmap.ultrasonics.frontRightPingPort, robotmap.ultrasonics.frontRightEchoPort)
        self.enabled = False

    def initDefaultCommand(self):
        print(self.logPrefix + "setting default command to PrintUltrasonicRange()")

    def enable(self):
        self.enabled = True
        self.frontLeft.setAutomaticMode(True)

    def disable(self):
        self.enabled = False
        self.frontLeft.setAutomaticMode(False)

    def getFrontDistance(self):
        # if(self.frontLeft.isRangeValid()):
        #    frontLeft = self.frontLeft.getRangeInches()

        if self.frontLeft.isRangeValid():
            frontLeft = self.frontLeft.getRangeInches()
        else:
            frontLeft = 0

        if self.frontRight.isRangeValid():
            frontRight = self.frontRight.getRangeInches()
        else:
            frontRight = 0

        return (frontRight + frontLeft) / 2