from wpilib.command import Command

import robotmap
import subsystems


class ElevatorMoveS1ToBottom(Command):

    def __init__(self):
        super().__init__('ElevatorMoveS1ToBottom')
        self.requires(subsystems.elevator)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

    def initialize(self):
        print("CMD ElevatorMoveS1ToBottom: Starting")

    def execute(self):
        subsystems.elevator.move(robotmap.elevator.s1AutoMoveDownSpeed, 0.0)

    def isFinished(self):
        return subsystems.elevator.s1BottomLimit()

    def end(self):
        subsystems.elevator.stopElevator()
        print("CMD ElevatorMoveS1ToBottom: Ended")

    def interrupted(self):
        subsystems.elevator.stopElevator()
        print("CMD ElevatorMoveS1ToBottom: Interrupted")



