import wpilib
from wpilib.ultrasonic import Ultrasonic
from wpilib.command.subsystem import Subsystem
import subsystems
import robotmap


class Ultrasonics(Subsystem):

    def __init__(self):
        print('Ultrasonics: init called')
        super().__init__('Ultrasonics')
        self.debug = False
        self.logPrefix = "Ultrasonics: "
        self.frontLeft = Ultrasonic(robotmap.ultrasonics.frontRightPingPort, robotmap.ultrasonics.frontRightEchoPort)
        self.enabled = False

    def enable(self):
        self.enabled = True
        self.frontLeft.setAutomaticMode(True)

    def disable(self):
        self.enabled = False
        self.frontLeft.setAutomaticMode(False)

    def getFrontDistance(self):
        #if(self.frontLeft.isRangeValid()):
        #    frontLeft = self.frontLeft.getRangeInches()

        if (self.frontRight.isRangeValid()):
            frontRight = self.frontLeft.getRangeInches()

        frontLeft = frontRight  #since we don't have left yet...
        return (frontRight + frontLeft) / 2