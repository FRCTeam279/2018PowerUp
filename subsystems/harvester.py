import wpilib
from wpilib.command.subsystem import Subsystem
from wpilib import Relay


class Harvester(Subsystem):

    def __init__(self):
        super().__init__('Harvester')
        print("Harvester Called")
        self.logPrefix = "Harvester"
        self.cubeinator3000 = Relay(0, Relay.Direction.kBoth)
