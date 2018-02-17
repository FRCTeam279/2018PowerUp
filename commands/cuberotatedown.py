from wpilib.command import Command

import wpilib
import io

import robotmap
import subsystems
from wpilib import Relay


class CubeRotateDown(Command):

    def __init__(self):
        super().__init__('CubeRotateDown')
        self.requires(subsystems.harvester)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

    def execute(self):
        subsystems.harvester.rotateDown(robotmap.harvester.rotateDownSpeed)

    def isFinished(self):
        return False

    def interrupted(self):
        subsystems.harvester.stopRotator()

    def end(self):
        subsystems.harvester.stopRotator()
