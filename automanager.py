import wpilib
from wpilib.smartdashboard import SmartDashboard


class AutoManager:
    """
    preferred element:
        'crossLine' - cross auto line
        'switch - prefer switch
        'scale' - prefer scale
    starting side:
        'left'
        'middle'
        'right'
    """
    def __init__(self):
        self.preferredElement = None
        self.startingPosition = None
        self.initialized = False

    def initialize(self):
        # initializing auto chooser
        self.preferredElement = wpilib.SendableChooser()
        self.preferredElement.addObject('crossLine', 0)
        self.preferredElement.addObject('switch', 1)
        self.preferredElement.addObject('scale', 2)

        self.startingPosition = wpilib.SendableChooser()
        self.startingPosition.addObject('left', 0)
        self.startingPosition.addObject('middle', 1)
        self.startingPosition.addObject('right', 2)

        SmartDashboard.putData("Preferred Element", self.preferredElement)
        SmartDashboard.putData("Starting Position", self.startingPosition)
        self.initialized = True

    def getStartingPosition(self):
        return self.startingPosition.getSelected()

    def getPreferredElement(self):
        return self.preferredElement.getSelected()
