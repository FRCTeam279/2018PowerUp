from wpilib.command import Command

import wpilib
import io

import robotmap
import subsystems
from wpilib import Relay


class CubeRotateUp(Command):

    def __init__(self):
        super().__init__('CubeRotateUp')
        self.requires(subsystems.harvester)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

    def execute(self):
        subsystems.harvester.rotateUp(robotmap.harvester.rotateUpSpeed)

    def isFinished(self):
        return False

    def interrupted(self):
        subsystems.harvester.stopRotator()

    def end(self):
        subsystems.harvester.stopRotator()
