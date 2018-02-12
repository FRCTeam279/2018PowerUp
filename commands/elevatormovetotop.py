from wpilib.command import Command

import robotmap
import subsystems


class ElevatorMoveToTop(Command):

    def __init__(self):
        super().__init__('ElevatorMoveToTop')
        self.requires(subsystems.elevator)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

    def initialize(self):
        print("CMD ElevatorMoveToTop: Starting")

    def execute(self):
        subsystems.elevator.move(robotmap.elevator.s1AutoMoveUpSpeed, robotmap.elevator.s2AutoMoveUpSpeed)

    def isFinished(self):
        return subsystems.elevator.s1TopLimit() and subsystems.elevator.s2TopLimit()

    def end(self):
        subsystems.elevator.stopElevator()
        print("CMD ElevatorMoveToTop: Ended")

    def interrupted(self):
        subsystems.elevator.stopElevator()
        print("CMD ElevatorMoveToTop: Interrupted")



