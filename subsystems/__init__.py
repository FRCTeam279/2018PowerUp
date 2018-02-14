'''
All subsystems should be imported here and instantiated inside the init method.
If you want your subsystem to be accessible to commands, you must add a variable
for it in the global scope.
'''

from wpilib.robotbase import RobotBase

from subsystems.climber import Climber
from subsystems.elevator import Elevator
from subsystems.harvester import Harvester
from subsystems.ultrasonics import Ultrasonics
from .tankdrive import TankDrive

driveline = None
elevator = None
harvester = None
#ultrasonics = None
climber = None

def init():
    print('Subsystems init called')
    '''
    Creates all subsystems. You must run this before any commands are
    instantiated. Do not run it more than once.
    '''
    global driveline
    global elevator
    global harvester
    global ultrasonics
    global climber

    '''
    Some tests call startCompetition multiple times, so don't throw an error if
    called more than once in that case.
    '''
    if (driveline) is not None and not RobotBase.isSimulation():
        raise RuntimeError('Subsystems have already been initialized')

    driveline = TankDrive()
    elevator = Elevator()
    harvester = Harvester()
    ultrasonics = Ultrasonics()
    climber = Climber()

