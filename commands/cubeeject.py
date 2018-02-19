from wpilib.command import Command

import wpilib
import io
import subsystems
from wpilib import Relay


class CubeEject(Command):

    def __init__(self):
        super().__init__('CubeEject')
        self.requires(subsystems.harvester)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

    def execute(self):
        subsystems.harvester.cubeinator3000.set(Relay.Value.kForward)

    def isFinished(self):
        return False

    def interrupted(self):
        subsystems.harvester.cubeinator3000.set(Relay.Value.kOff)
