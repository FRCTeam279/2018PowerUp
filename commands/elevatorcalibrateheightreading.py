from wpilib.command import CommandGroup, PrintCommand

import robotmap
import subsystems
from commands.delay import Delay
from commands.elevatormovetobottom import ElevatorMoveToBottom
from commands.elevatormovetotop import ElevatorMoveToTop



class ElevatorCalibrateHeightReading(CommandGroup):

    def __init__(self):
        super().__init__('ElevatorCalibrateHeightReading')
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)

        self.addSequential(PrintCommand("CMD Group ElevatorCalibrateHeightReading: Starting"))

        self.addSequential(ElevatorMoveToTop())
        self.addSequential(Delay(500))
        self.addSequential(PrintCommand("CMD Group ElevatorCalibrateHeightReading: Top Voltage = {}".format(
            subsystems.elevator.getHeightVoltage())))

        self.addSequential(ElevatorMoveToBottom())
        self.addSequential(Delay(500))
        self.addSequential(PrintCommand("CMD Group ElevatorCalibrateHeightReading: Bottom Voltage = {}".format(
            subsystems.elevator.getHeightVoltage())))

        self.addSequential(ElevatorMoveToTop())
        self.addSequential(Delay(500))
        self.addSequential(PrintCommand("CMD Group ElevatorCalibrateHeightReading: Top Voltage = {}".format(
            subsystems.elevator.getHeightVoltage())))

        self.addSequential(ElevatorMoveToBottom())
        self.addSequential(Delay(500))
        self.addSequential(PrintCommand("CMD Group ElevatorCalibrateHeightReading: Bottom Voltage = {}".format(
            subsystems.elevator.getHeightVoltage())))

        self.addSequential(ElevatorMoveToTop())
        self.addSequential(Delay(500))
        self.addSequential(PrintCommand("CMD Group ElevatorCalibrateHeightReading: Top Voltage = {}".format(
            subsystems.elevator.getHeightVoltage())))

        self.addSequential(ElevatorMoveToBottom())
        self.addSequential(Delay(500))
        self.addSequential(PrintCommand("CMD Group ElevatorCalibrateHeightReading: Bottom Voltage = {}".format(
            subsystems.elevator.getHeightVoltage())))

        self.addSequential(PrintCommand("CMD Group ElevatorCalibrateHeightReading: Completed"))



