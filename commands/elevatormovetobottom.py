from wpilib.command import Command

import robotmap
import subsystems


class ElevatorMoveToBottom(Command):

    def __init__(self):
        super().__init__('ElevatorMoveToBottom')
        self.requires(subsystems.elevator)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

    def initialize(self):
        print("CMD ElevatorMoveToBottom: Starting")

    def execute(self):
        subsystems.elevator.move(robotmap.elevator.s1AutoMoveDownSpeed, robotmap.elevator.s2AutoMoveDownSpeed)

    def isFinished(self):
        return subsystems.elevator.s1BottomLimit() and subsystems.elevator.s2BottomLimit()

    def end(self):
        subsystems.elevator.stopElevator()
        print("CMD ElevatorMoveToBottom: Ended")

    def interrupted(self):
        subsystems.elevator.stopElevator()
        print("CMD ElevatorMoveToBottom: Interrupted")



