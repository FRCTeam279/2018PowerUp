from wpilib.command import Command

import robotmap
import subsystems


class ElevatorMoveS1ToTop(Command):

    def __init__(self):
        super().__init__('ElevatorMoveS1ToTop')
        self.requires(subsystems.elevator)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

    def initialize(self):
        print("CMD ElevatorMoveS1ToTop: Starting")

    def execute(self):
        subsystems.elevator.move(robotmap.elevator.s1AutoMoveUpSpeed, 0.0)

    def isFinished(self):
        return subsystems.elevator.s1TopLimit()

    def end(self):
        subsystems.elevator.stopElevator()
        print("CMD ElevatorMoveS1ToTop: Ended")

    def interrupted(self):
        subsystems.elevator.stopElevator()
        print("CMD ElevatorMoveS1ToTop: Interrupted")



