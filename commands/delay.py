import time
from wpilib.command import Command


class Delay(Command):
    """
    This command does nothing for X milliseconds
    """

    def __init__(self, delayMilliseconds):
        super().__init__('Delay')
        self.setInterruptible(True)
        self.setRunWhenDisabled(True)
        self.delayMilliseconds = delayMilliseconds
        self.endTime = 0

    def initialize(self):
        self.endTime = int(round(time.time() * 1000)) + self.delayMilliseconds

    def execute(self):
        pass

    def isFinished(self):
        if int(round(time.time() * 1000)) > self.endTime:
            return True
        return False

    def end(self):
        self.endTime = 0

    def interrupted(self):
        self.endTime = 0


