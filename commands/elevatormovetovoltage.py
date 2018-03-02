from wpilib.command import Command

import robotmap
import subsystems


class ElevatorMoveToVoltage(Command):

    def __init__(self, targetVoltage):
        super().__init__('ElevatorMoveToVoltage')
        self.requires(subsystems.elevator)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
        self.s1Speed = 0.0
        self.s2Speed = 0.0
        self.moveDirection = 0.0
        self.targetVoltage = targetVoltage

    def initialize(self):
        print("CMD ElevatorMoveToVoltage: Starting")
        currentVoltage = subsystems.elevator.getHeightVoltage()

        if self.targetVoltage > currentVoltage:
            self.moveDirection = 1
            self.s1Speed = robotmap.elevator.s1AutoMoveUpSpeed
            self.s2Speed = robotmap.elevator.s2AutoMoveUpSpeed
        else:
            self.moveDirection = -1
            self.s1Speed = robotmap.elevator.s1AutoMoveDownSpeed
            self.s2Speed = robotmap.elevator.s12AutoMoveDownSpeed

    def execute(self):
        subsystems.elevator.move(self.s1Speed, self.s2Speed)

    def isFinished(self):
        if self.moveDirection == 1.0:
            return subsystems.elevator.getHeightVoltage() > self.targetVoltage
        else:
            return subsystems.elevator.getHeightVoltage() < self.targetVoltage

    def end(self):
        subsystems.elevator.holdElevator()
        print("CMD ElevatorMoveToVoltage: Ended. target={}, current{}".format(self.targetVoltage, subsystems.elevator.getHeightVoltage()))

    def interrupted(self):
        subsystems.elevator.holdElevator()
        print("CMD ElevatorMoveToVoltage: Interruptedtarget={}, current{}".format(self.targetVoltage, subsystems.elevator.getHeightVoltage()))




