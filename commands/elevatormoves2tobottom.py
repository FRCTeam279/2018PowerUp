from wpilib.command import Command

import robotmap
import subsystems


class ElevatorMoveS2ToBottom(Command):

    def __init__(self):
        super().__init__('ElevatorMoveS2ToBottom')
        self.requires(subsystems.elevator)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

    def initialize(self):
        print("CMD ElevatorMoveS2ToBottom: Starting")

    def execute(self):
        subsystems.elevator.move(0.0, robotmap.elevator.s2AutoMoveDownSpeed)

    def isFinished(self):
        return subsystems.elevator.s2BottomLimit()

    def end(self):
        subsystems.elevator.stopElevator()
        print("CMD ElevatorMoveS2ToBottom: Ended")

    def interrupted(self):
        subsystems.elevator.stopElevator()
        print("CMD ElevatorMoveS2ToBottom: Interrupted")



