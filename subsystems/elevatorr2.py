import math
import wpilib
from wpilib.command.subsystem import Subsystem

import subsystems
import robotmap
from commands.elevatorteleoprun import ElevatorTeleopRun


class ElevatorR2(Subsystem):

    def __init__(self):
        print('ElevatorR2: init called')
        super().__init__('ElevatorR2')
        self.debug = False

        # self._heightPot = wpilib.AnalogInput(robotmap.elevator.heightPotPort)

        self._s1TopLimit = wpilib.DigitalInput(robotmap.elevator.s1TopLimitPort)
        self._s1BottomLimit = wpilib.DigitalInput(robotmap.elevator.s1BottomLimitPort)
        self._s1SpdController = wpilib.VictorSP(robotmap.elevator.s1SpdControllerPort)
        self._s1SpdController.setInverted(robotmap.elevator.s1SpdControllerReverse)

        self._s2TopLimit = wpilib.DigitalInput(robotmap.elevator.s2TopLimitPort)
        self._s2BottomLimit = wpilib.DigitalInput(robotmap.elevator.s2BottomLimitPort)
        self._s2SpdController = wpilib.VictorSP(robotmap.elevator.s2SpdControllerPort)
        self._s2SpdController.setInverted(robotmap.elevator.s2SpdControllerReverse)

        self._heightPot = wpilib.AnalogInput(robotmap.elevator.heightPotPort)

        self._s1LastSpeedSet = 0.0
        self._s2LastSpeedSet = 0.0

    def initDefaultCommand(self):
        self.setDefaultCommand(ElevatorTeleopRun())


    # =================================================================================================================
    # Shared Functions
    # =================================================================================================================

    def stopElevator(self):
        self._s1SpdController.set(0.0)
        self._s2SpdController.set(0.0)

    def holdElevator(self):
        self._s1SpdController.set(robotmap.elevator.s1HoldingSpeed)
        self._s2SpdController.set(robotmap.elevator.s2HoldingSpeed)
        #self._s1LastSpeedSet = robotmap.elevator.s1HoldingSpeed
        #self._s2LastSpeedSet = robotmap.elevator.s2HoldingSpeed

    def getHeightInches(self):
        return self._heightPot.getAverageVoltage() * robotmap.elevator.heightVoltsPerInch

    def getHeightVoltage(self):
        return self._heightPot.getAverageVoltage()

    # avoid using this - seriously
    def rawMove(self, speed):
        self._s1SpdController.set(speed)
        self._s2SpdController.set(speed)

    # =================================================================================================================
    # Approach Two - Holding Speed
    # =================================================================================================================
    # These methods allow movement based on whether or not the limit switches at the extent of each assemble are
    # are triggered.
    # However, rather than have the baseline speed set at 0.0, it uses the "holding speed" for each stage as the
    # baseline speed to go up for down from via the speed sent from the drivers joystick (or auto command).
    # In theory, this means when the driver takes their hands off the stick, the elevator shouldn't move
    # In reality, it will likely drift up or down depending on if there is a crate on it, or other factors that change
    # the performance of the system.
    # Example:
    #   It is found that the second stage will hold steady if %10 power is applied to the motor
    #   The driver wants to move the harvester down at %30 (based on his stick movement)
    #   The actual speed sent to the speed controller is -%20
    #               10% (holding speed) - 30% desired motion = 20% down power
    #
    # Adjust the holding speeds in the robotmap

    def move(self, s1Speed, s2Speed):
        if s1Speed == 0.0:
            s1Speed = robotmap.elevator.s1HoldingSpeed

        if s2Speed == 0.0:
            s2Speed = robotmap.elevator.s2HoldingSpeed

        self.s1Move(s1Speed)
        self.s2Move(s2Speed)

    def s1Move(self, speed):
        if speed >= 0.0:
            self.s1MoveUp(speed)
        else:
            self.s1MoveDown(speed)

    def s2Move(self, speed):
        if speed >= 0.0:
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
                self._s1SpdController.set(0.0)
                return
            else:
                self._s1SpdController.set(robotmap.elevator.s1HoldingSpeed)
                return

        if not self.s1TopLimit():
            speed = math.fabs(speed)
            speed = robotmap.elevator.s1HoldingSpeed + (robotmap.elevator.s1ScaleSpeedUp * speed)

            self._s1SpdController.set(speed)
        else:
            self._s1SpdController.set(robotmap.elevator.s1HoldingSpeed)

    def s1MoveDown(self, speed):
        if not self.s1BottomLimit():
            speed = math.fabs(speed)
            speed = robotmap.elevator.s1HoldingSpeed - (robotmap.elevator.s1ScaleSpeedDown * speed)
            self._s1SpdController.set(speed)
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
            speed = robotmap.elevator.s2HoldingSpeed + (robotmap.elevator.s2ScaleSpeedUp * speed)
            self._s2SpdController.set(speed)
        else:
            self._s2SpdController.set(robotmap.elevator.s1HoldingSpeed)

    def s2MoveDown(self, speed):
        # S1 should be drive down before S2
        # we only want to let the harvester move down if the middle stage is already all the way down
        # If S1 happens to be in the middle (which should not be the case, but could happen...), use a holding speed
        if not self.s1BottomLimit():
            if self.s2BottomLimit():
                self._s2SpdController.set(0.0)
                return
            else:
                self._s2SpdController.set(robotmap.elevator.s2HoldingSpeed)
                return

        if not self.s2BottomLimit():
            speed = math.fabs(speed)
            speed = robotmap.elevator.s2HoldingSpeed - (robotmap.elevator.s2ScaleSpeedDown * speed)
            self._s2SpdController.set(speed)
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



