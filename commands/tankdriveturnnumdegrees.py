from wpilib.command import Command

import subsystems


class TankDriveTurnNumDegrees(Command):
    """
    This command does nothing for X milliseconds
    """

    def __init__(self, degDiff):
        super().__init__('TankDriveTurnNumDegrees')
        self.requires(subsystems.driveline)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
        self.degDiff = degDiff

    def initialize(self):
        pass

    def execute(self):
        pass

    def isFinished(self):
        return True

    def end(self):
        pass

    def interrupted(self):
        pass
