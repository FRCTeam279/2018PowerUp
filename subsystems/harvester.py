import wpilib
from wpilib.ultrasonic import Ultrasonic
from wpilib.command.subsystem import Subsystem
import subsystems
import robotmap


class Harvester(Subsystem):

    def __init__(self):
        print('Harvester: init called')
        super().__init__('Harvester')
        self.debug = False
        self.logPrefix = "Harvester: "