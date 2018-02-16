from wpilib.command import Command

import wpilib
import io
import subsystems
from wpilib import Relay


class GrabCube(Command):

    def __init__(self):
        super().__init__('GrabCube')
        self.requires(subsystems.harvester)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

    def execute(self):
        subsystems.harvester.cubegraberinator3000.set(Relay.Value.kForward)

    def isFinished(self):
        return False

    def interrupted(self):
        subsystems.harvester.cubegrabinator3000.set(Relay.Value.kOff)
