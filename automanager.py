import wpilib
from wpilib.smartdashboard import SmartDashboard

from commands.autodriveforwardtoswitch import AutoDriveForwardToSwitch
from commands.autoloadscaletoleft import AutoLoadScaleToLeft
from commands.autoloadscaletoright import AutoLoadScaleToRight
from commands.autoloadswitchfrommid import AutoLoadSwitchFromMid
from commands.autoloadswitchtoleftfromside import AutoLoadSwitchToLeftFromSide
from commands.autoloadswitchtorightfromside import AutoLoadSwitchToRightFromSide

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

        self.gameData = None
        self.gameDataNearSwitchSide = None
        self.gameDataScaleSide = None

    def initialize(self):
        if self.initialized:
            return

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
        print("AutoManager: Initialized")
        self.initialized = True

    def getStartingPosition(self):
        return self.startingPosition.getSelected()

    def getPreferredElement(self):
        return self.preferredElement.getSelected()

    # parameters are the L or R for each object from game data
    def getAction(self, nearSwitchSide, scaleSide):

        # ---------------------------------------------
        # Middle Starting Spot
        # ---------------------------------------------
        if self.getStartingPosition() == 'middle':
            print("AutoManager.GetAction: Starting in middle, nearSwitchSide={}, returning AutoLoadSwitchToLeftFromMid".format(nearSwitchSide))
            return AutoLoadSwitchFromMid(nearSwitchSide)

        # ---------------------------------------------
        # Left Starting Spot
        # ---------------------------------------------
        if self.getStartingPosition() == 'left':

            if self.getPreferredElement() == 'crossLine':
                print("AutoManager.GetAction: AutoDriveForward - Preferred={}, Starting={}, NearSwitch={}, Scale={}".format(
                        self.getPreferredElement(), self.getStartingPosition(), nearSwitchSide, scaleSide))
                return AutoDriveForwardToSwitch()

            if self.getPreferredElement() == 'switch' and nearSwitchSide=='L':
                print("AutoManager.GetAction: AutoLoadSwitchToLeftFromSide - Preferred={}, Starting={}, NearSwitch={}, Scale={}".format(
                        self.getPreferredElement(), self.getStartingPosition(), nearSwitchSide, scaleSide))
                return AutoLoadSwitchToLeftFromSide()

            if self.getPreferredElement() == 'scale' and scaleSide=='L':
                print("AutoManager.GetAction: AutoLoadScaleToLeft - Preferred={}, Starting={}, NearSwitch={}, Scale={}".format(
                        self.getPreferredElement(), self.getStartingPosition(), nearSwitchSide, scaleSide))
                return AutoLoadScaleToLeft()

            # Fall back number 1 - the other element
            # if the preferred element isn't on this side
            #  return either of the others if they are...
            if (self.getPreferredElement() == 'switch' and nearSwitchSide != 'L') or (
                            self.getPreferredElement() == 'scale' and scaleSide != 'L'):
                if nearSwitchSide=='L':
                    print("AutoManager.GetAction: AutoLoadSwitchToLeftFromSide - Preferred={}, Starting={}, NearSwitch={}, Scale={}".format(
                            self.getPreferredElement(), self.getStartingPosition(), nearSwitchSide, scaleSide))
                    return AutoLoadSwitchToLeftFromSide()
                if scaleSide == 'L':
                    print("AutoManager.GetAction: AutoLoadScaleToLeft - Preferred={}, Starting={}, NearSwitch={}, Scale={}".format(
                            self.getPreferredElement(), self.getStartingPosition(), nearSwitchSide, scaleSide))
                    return AutoLoadScaleToLeft()

        # ---------------------------------------------
        # Left Starting Spot
        # ---------------------------------------------
        if self.getStartingPosition() == 'right':
            if self.getPreferredElement() == 'crossLine':
                print("AutoManager.GetAction: AutoDriveForward - Preferred={}, Starting={}, NearSwitch={}, Scale={}".format(
                        self.getPreferredElement(), self.getStartingPosition(), nearSwitchSide, scaleSide))
                return AutoDriveForwardToSwitch()

            if self.getPreferredElement() == 'switch' and nearSwitchSide=='R':
                print("AutoManager.GetAction: AutoLoadSwitchToRightFromSide - Preferred={}, Starting={}, NearSwitch={}, Scale={}".format(
                        self.getPreferredElement(), self.getStartingPosition(), nearSwitchSide, scaleSide))
                return AutoLoadSwitchToRightFromSide()

            if self.getPreferredElement() == 'scale' and scaleSide=='R':
                print("AutoManager.GetAction: AutoLoadScaleToRight - Preferred={}, Starting={}, NearSwitch={}, Scale={}".format(
                        self.getPreferredElement(), self.getStartingPosition(), nearSwitchSide, scaleSide))
                return AutoLoadScaleToRight()

            # Fall back number 1 - the other element
            # if the preferred element isn't on this side
            #  return either of the others if they are...
            if (self.getPreferredElement() == 'switch' and nearSwitchSide != 'R') or (
                            self.getPreferredElement() == 'scale' and scaleSide != 'R'):
                if nearSwitchSide=='R':
                    print("AutoManager.GetAction: AutoLoadSwitchToRightFromSide - Preferred={}, Starting={}, NearSwitch={}, Scale={}".format(
                            self.getPreferredElement(), self.getStartingPosition(), nearSwitchSide, scaleSide))
                    return AutoLoadSwitchToRightFromSide()
                if scaleSide == 'R':
                    print("AutoManager.GetAction: AutoLoadScaleToRight - Preferred={}, Starting={}, NearSwitch={}, Scale={}".format(
                            self.getPreferredElement(), self.getStartingPosition(), nearSwitchSide, scaleSide))
                    return AutoLoadScaleToRight()

        # ---------------------------------------------
        # Fall back number 2 - cross the line
        # ---------------------------------------------
        print(
            "AutoManager.GetAction: Defaulting to CrossLine - Preferred={}, Starting={}, NearSwitch={}, Scale={}".format(
                self.getPreferredElement(), self.getStartingPosition(), nearSwitchSide, scaleSide))
        return AutoDriveForwardToSwitch()

