import wpilib
from wpilib.command.subsystem import Subsystem

import robotmap
from commands.climberteleoprun import ClimberTeleopRun


class Climber(Subsystem):

    def __init__(self):
        print('Climber: init called')
        super().__init__('Climber')
        self.debug = False
        self.logPrefix = "Climber: "

        self._spdController = wpilib.VictorSP(robotmap.climber.spdControllerPort)
        self._spdController.setInverted(robotmap.climber.spdControllerReverse)
        print('Climber Subsystem Initiated')

    def stopClimbing(self):
        self._spdController.set(0.0)

    def climbUp(self, speed):
        self._spdController.set(speed)

    def climbDown(self, speed):
        self._spdController.set(speed)

    def initDefaultCommand(self):
        self.setDefaultCommand(ClimberTeleopRun())
