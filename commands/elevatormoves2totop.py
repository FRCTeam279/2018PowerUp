from wpilib.command import Command

import robotmap
import subsystems


class ElevatorMoveS2ToTop(Command):

    def __init__(self):
        super().__init__('ElevatorMoveS2ToTop')
        self.requires(subsystems.elevator)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

    def initialize(self):
        print("CMD ElevatorMoveS2ToTop: Starting")

    def execute(self):
        subsystems.elevator.move(0.0, robotmap.elevator.s2AutoMoveUpSpeed)

    def isFinished(self):
        return subsystems.elevator.s2TopLimit()

    def end(self):
        subsystems.elevator.stopElevator()
        print("CMD ElevatorMoveS2ToTop: Ended")

    def interrupted(self):
        subsystems.elevator.stopElevator()
        print("CMD ElevatorMoveS2ToTop: Interrupted")



