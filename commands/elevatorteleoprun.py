from wpilib.command import Command

import subsystems
import oi

class ElevatorTeleopRun(Command):

    def __init__(self):
        super().__init__('ElevatorTeleopRun')
        self.requires(subsystems.elevator)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
        self.logCounter = 0

    def execute(self):
        speed = -(oi.goGamePad.getRawAxis(oi.config.axisElevator))
        speed = oi.filterInput(speed, deadZone=oi.config.goGamePadNullZone,
                               filterFactor=oi.config.goGamePadStickFilterFactor, scale=oi.config.goGamePadStickScale)

        subsystems.elevator.move(speed, speed)

    def isFinished(self):
        return False

    def end(self):
        subsystems.elevator.stopElevator()

    def interrupted(self):
        subsystems.elevator.stopElevator()



