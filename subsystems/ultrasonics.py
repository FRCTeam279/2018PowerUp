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
        try:
            self.frontLeft = Ultrasonic(robotmap.ultrasonics.frontLeftPingPort, robotmap.ultrasonics.frontLeftEchoPort)
        except:
            print("Ultrasonics: Error!!! Could not create front left ultrasonic!")
        try:
            self.frontRight = Ultrasonic(robotmap.ultrasonics.frontRightPingPort, robotmap.ultrasonics.frontRightEchoPort)
        except:
            print("Ultrasonics: Error!!! Could not create front right ultrasonic!")
        self.enabled = False

    def enable(self):
        self.enabled = True
        # if self.frontLeft:
        self.frontLeft.setAutomaticMode(True)
        self.frontLeft.setEnabled(True)
        # if self.frontRight:
        self.frontRight.setEnabled(True)
        self.frontLeft.setAutomaticMode(True)

    def disable(self):
        self.enabled = False
        if self.frontLeft:
            self.frontLeft.setEnabled(False)
        if self.frontRight:
            self.frontRight.setEnabled(False)

    def getFrontDistance(self):
        frontLeft = -1
        if self.frontLeft:
            if self.frontLeft.isRangeValid():
                frontLeft = self.frontLeft.getRangeInches()
                if frontLeft < 7:  #the cubinator3000 is in the way
                    frontLeft = -1

        frontRight = -1
        if self.frontRight:
            if self.frontRight.isRangeValid():
                frontRight = self.frontRight.getRangeInches()
                if frontRight < 7: #the cubinator3000 is in the way
                    frontRight = -1

        if frontLeft >= 0 and frontRight >= 0:
            return (frontRight + frontLeft) / 2
        elif frontLeft >= 0:
            return frontLeft
        elif frontRight >= 0:
            return frontRight
        else:
            return 0
