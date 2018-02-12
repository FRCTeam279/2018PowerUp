import wpilib
from wpilib.command.subsystem import Subsystem
import subsystems
import robotmap


class Climber(Subsystem):

    def __init__(self):
        print('Climber: init called')
        super().__init__('Climber')
        self.debug = False
        self.logPrefix = "Climber: "

        self._spdController = wpilib.VictorSP(robotmap.climber.spdControllerPort)