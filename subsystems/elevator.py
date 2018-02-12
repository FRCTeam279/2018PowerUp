import math
import wpilib
from wpilib.command.subsystem import Subsystem

import subsystems
import robotmap
from commands.elevatorteleoprun import ElevatorTeleopRun


class Elevator(Subsystem):

    def __init__(self):
        print('Elevator: init called')
        super().__init__('Elevator')
        self.debug = False

        # self._heightPot = wpilib.AnalogInput(robotmap.elevator.heightPotPort)

        self._s1TopLimit = wpilib.DigitalInput(robotmap.elevator.s1TopLimitPort)
        self._s1BottomLimit = wpilib.DigitalInput(robotmap.elevator.s1BottomLimitPort)
        self._s1SpdController = wpilib.VictorSP(robotmap.elevator.s1SpdControllerPort)

        self._s2TopLimit = wpilib.DigitalInput(robotmap.elevator.s2TopLimitPort)
        self._s2BottomLimit = wpilib.DigitalInput(robotmap.elevator.s2BottomLimitPort)
        self._s2SpdController = wpilib.VictorSP(robotmap.elevator.s2SpdControllerPort)

    def initDefaultCommand(self):
        self.setDefaultCommand(ElevatorTeleopRun())

    # =================================================================================================================
    # Shared Functions
    # =================================================================================================================

    def stopElevator(self):
        self._s1SpdController.set(0.0)
        self._s2SpdController.set(0.0)

    def getHeight(self):
        # return self._heightPot.get() * robotmap.elevator.heightVoltsPerInch
        pass

    def rawMove(self, speed):
        self._s1SpdController.set(speed)
        self._s2SpdController.set(speed)

    # =================================================================================================================
    # Approach One - Simple Movement
    # =================================================================================================================
    # These methods are used to drive up or down solely based on the limit switches and desired speed
    # All maintaining of height must be done by the driver
    #
    # Use the holding speed to set speed up for S1 and S2 if the top switch is triggered

    def move(self, s1Speed, s2Speed):
        self.s1Move(s1Speed)
        self.s2Move(s2Speed)

    def s1Move(self, speed):
        if speed >= 0.0:
            self.s1MoveUp(speed)
        else:
            self.s1MoveDown(speed)

    def s2Move(self, speed):
        if speed > 0.0:
            self.s2MoveUp(speed)
        else:
            self.s2MoveDown(speed)

    # --------------------------------------
    # Stage 1
    # --------------------------------------
    def s1MoveUp(self, speed):
        # We only want to move stage 1 up if stage 2 is maxed out
        #  in other words the inner portion moving the harvester gets to top first, and then we allow outer
        #  extension to move up
        #  this keeps center of gravity lower
        # If S1 happens to be in the middle (which should not be the case, but could happen...), use a holding speed
        if not self.s2TopLimit():
            if self.s1BottomLimit():
                return
            else:
                self._s1SpdController.set(robotmap.elevator.s1HoldingSpeed)
                return

        # now for the actual movement since we know the harvester must be at the top if we reached this point
        if not self.s1TopLimit():
            speed = math.fabs(speed)
            speed = robotmap.elevator.s1ScaleSpeedUp * speed
            self._s1SpdController.set(speed)
        else:
            # If we are already at the top.. just hold
            self._s1SpdController.set(robotmap.elevator.s1HoldingSpeed)

    def s1MoveDown(self, speed):
        if not self.s1BottomLimit():
            speed = math.fabs(speed)
            speed = robotmap.elevator.s1ScaleSpeedDown * speed
            self._s1SpdController.set(-speed)
        else:
            self._s1SpdController.set(0.0)

    def s1TopLimit(self):
        if robotmap.elevator.s1TopLimitNormalClosed:
            return not self._s1TopLimit.get()
        else:
            return self._s1TopLimit.get()

    def s1BottomLimit(self):
        if robotmap.elevator.s1BottomLimitNormalClosed:
            return not self._s1BottomLimit.get()
        else:
            return self._s1BottomLimit.get()

    # ----------------------------------------------------------------------------------------------------------------
    # Stage 2
    # ----------------------------------------------------------------------------------------------------------------
    def s2MoveUp(self, speed):
        if not self.s2TopLimit():
            speed = math.fabs(speed)
            speed = robotmap.elevator.s2ScaleSpeedUp * speed
            self._s2SpdController.set(speed)
        else:
            # If we are already at the top.. just hold
            self._s2SpdController.set(robotmap.elevator.s2HoldingSpeed)

    def s2MoveDown(self, speed):
        # we only want to let the harvester move down if the middle stage is already all the way down
        # If S1 happens to be in the middle (which should not be the case, but could happen...), use a holding speed
        if not self.s1BottomLimit():
            if self.s2BottomLimit():
                self._s2SpdController.set(0.0)
                return
            else:
                self._s1SpdController.set(robotmap.elevator.s1HoldingSpeed)
                return

        # and now the planned movement - S1 must already have been driven the middle assembly all the way down
        if not self.s2BottomLimit():
            speed = math.fabs(speed)
            speed = robotmap.elevator.s2ScaleSpeedDown * speed
            self._s2SpdController.set(-speed)
        else:
            self._s2SpdController.set(0.0)

    def s2TopLimit(self):
        if robotmap.elevator.s2TopLimitNormalClosed:
            return not self._s2TopLimit.get()
        else:
            return self._s2TopLimit.get()

    def s2BottomLimit(self):
        if robotmap.elevator.s2BottomLimitNormalClosed:
            return not self._s2BottomLimit.get()
        else:
            return self._s2BottomLimit.get()


