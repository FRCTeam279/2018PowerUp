from wpilib.command import Command

import oi
import subsystems


class ClimberTeleopRun(Command):
    
    def __init__(self):
        super().__init__('ClimberTeleopRun')
        self.requires(subsystems.climber)
        self.setInterruptible(True)
        self.setRunWhenDisabled(False)
        
    def execute(self):
        # TODO - validate if we're at the end of the match and ready to climb, should we require another button too??
        speed = oi.goGamePad.getRawAxis(oi.config.axisClimber)
        subsystems.climber.climbUp(speed)

    def isFinished(self):
        return False

    def interrupted(self):
        subsystems.climber.stopClimbing()

    def end(self):
        subsystems.climber.stopClimbing()
