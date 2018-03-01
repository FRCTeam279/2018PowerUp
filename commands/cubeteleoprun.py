from wpilib.command import Command

import subsystems
import oi


class CubeTeleopRun(Command):

    def __init__(self):
        super().__init__('CubeTeleopRun')
        self.requires(subsystems.harvester)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
        self.logCounter = 0

    def execute(self):
        if oi.goGamePad.getRawAxis(oi.config.axisCubeLoadLeft) > 0.5:
            subsystems.harvester.cubeIntakeLeft()
        elif oi.btnCubeEjectLeft.get():
            subsystems.harvester.cubeEjectLeft()
        else:
            subsystems.harvester.cubeStopLeft()

        if oi.goGamePad.getRawAxis(oi.config.axisCubeLoadRight) > 0.5:
            subsystems.harvester.cubeIntakeRight()
        elif oi.btnCubeEjectRight.get():
            subsystems.harvester.cubeEjectRight()
        else:
            subsystems.harvester.cubeStopRight()

    def isFinished(self):
        return False

    def end(self):
        subsystems.elevator.stopElevator()

    def interrupted(self):
        subsystems.elevator.stopElevator()



