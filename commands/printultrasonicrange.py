import wpilib
from wpilib.command import Command
import subsystems

class PrintUltrasonicRange(Command):
    """
    This command prints the ultrasonic range to the smartdashboard
    """

    def __init__(self):
        super().__init__('PrintUltrasonicRange')
        self.setInterruptible(True)
        self.setRunWhenDisabled(True)
        self.requires(subsystems.ultrasonics)

    def initialize(self):
        subsystems.ultrasonics.enable()

    def execute(self):
        Ultrasonics.getFrontDistance()

    def interrupted(self):
        Ultrasonics.disable()

    def end(self):
        Ultrasonics.disable()
