import math
import wpilib
from wpilib.command.subsystem import Subsystem
from wpilib import Relay
from wpilib import Spark

import robotmap
from commands.cubeteleoprun import CubeTeleopRun


class Harvester(Subsystem):

    def __init__(self):
        super().__init__('Harvester')
        print("Cubinator3000 (Harvester) Called")
        self.logPrefix = "Harvester: "
        try:
            #self.cubeinator3000Left = Relay(robotmap.harvester.relayPortLeft, Relay.Direction.kBoth)
            self.cubeinator3000Left = Spark(robotmap.harvester.motorPortLeft)
        except Exception as e:
            print("{}Exception caught instantiating Left relay. {}".format(self.logPrefix, e))
            if not wpilib.DriverStation.getInstance().isFmsAttached():
                raise

        try:
            #self.cubeinator3000Right = Relay(robotmap.harvester.relayPortRight, Relay.Direction.kBoth)
            self.cubeinator3000Right = Spark(robotmap.harvester.motorPortRight)
        except Exception as e:
            print("{}Exception caught instantiating Right relay. {}".format(self.logPrefix, e))
            if not wpilib.DriverStation.getInstance().isFmsAttached():
                raise

        try:
            self._rotator = wpilib.VictorSP(robotmap.harvester.rotationSpdPort)
            self._rotator.setInverted(robotmap.harvester.rotationSpdReverse)
        except Exception as e:
            print("{}Exception caught instantiating Rotator. {}".format(self.logPrefix, e))
            if not wpilib.DriverStation.getInstance().isFmsAttached():
                raise

    def cubeEjectLeft(self):
        #self.cubeinator3000Left.set(Relay.Value.kForward)
        self.cubeinator3000Left.set(robotmap.harvester.speed * -1.0)

    def cubeEjectRight(self):
        #self.cubeinator3000Right.set(Relay.Value.kForward)
        self.cubeinator3000Right.set(robotmap.harvester.speed * -1.0)

    def cubeIntakeLeft(self):
        #self.cubeinator3000Left.set(Relay.Value.kReverse)
        self.cubeinator3000Left.set(robotmap.harvester.speed)

    def cubeIntakeRight(self):
        #self.cubeinator3000Right.set(Relay.Value.kReverse)
        self.cubeinator3000Right.set(robotmap.harvester.speed)

    def cubeStopLeft(self):
        #self.cubeinator3000Left.set(Relay.Value.kOff)
        self.cubeinator3000Left.set(0.0)

    def cubeStopRight(self):
        #self.cubeinator3000Right.set(Relay.Value.kOff)
        self.cubeinator3000Right.set(0.0)

    def initDefaultCommand(self):
        self.setDefaultCommand(CubeTeleopRun())
        print("{}Default command set to CubeTeleopRun".format(self.logPrefix))

    def stopRotator(self):
        self._rotator.set(0.0)

    def rotateUp(self, speed):
        math.fabs(speed)
        self._rotator.set(speed)

    def rotateDown(self, speed):
        math.fabs(speed)
        self._rotator.set(-1.0 * speed)

