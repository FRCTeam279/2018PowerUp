import math

from wpilib.command import Command
import subsystems
import oi

class TankDriveTeleopDefaultSkid(Command):
    '''
    This command will read the joystick's y axis and use that value to control
    the speed of the SingleMotor subsystem.
    '''


    def __init__(self):
        super().__init__('TankDriveTeleopDefaultSkid')
        self.requires(subsystems.driveline)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
    

    def execute(self):

        subsystems.driveline.drive(oi.leftDriverStick.getY() * -1.0, oi.rightDriverStick.getY() * -1.0)

    def isFinished(self):
        return False
    
    
    