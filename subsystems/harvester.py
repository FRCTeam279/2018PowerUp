import math
import wpilib
from wpilib.command.subsystem import Subsystem
from wpilib import Relay

import robotmap


class Harvester(Subsystem):

    def __init__(self):
        super().__init__('Harvester')
        print("Cubinator3000 (Harvester) Called")
        self.logPrefix = "Harvester"
        self.cubeinator3000 = Relay(0, Relay.Direction.kBoth)

        self._rotator = wpilib.VictorSP(robotmap.harvester.rotationSpdPort)
        self._rotator.setInverted(robotmap.harvester.rotationSpdReverse)

    def stopRotator(self):
        self._rotator.set(0.0)

    def rotateUp(self, speed):
        math.fabs(speed)
        self._rotator.set(speed)

    def rotateDown(self, speed):
        math.fabs(speed)
        self._rotator.set(-1.0 * speed)

