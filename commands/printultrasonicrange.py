import wpilib
from wpilib.command import Command
import subsystems
from wpilib import SmartDashboard


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
        SmartDashboard.putNumber("Ultrasonic Distance", subsystems.ultrasonics.getFrontDistance())

    def interrupted(self):
        subsystems.ultrasonics.disable()

    def end(self):
        subsystems.ultrasonics.disable()
