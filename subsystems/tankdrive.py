import wpilib
from wpilib.command.subsystem import Subsystem

from commands.driveteleopdefaultskid import DriveTeleopDefaultSkid as DriveTeleopDefaultSkid
from commands.driveteleopdefaultnfs import DriveTeleopDefaultNFS as DriveTeleopDefaultNFS
import robotmap


class TankDrive(Subsystem):

    def __init__(self):
        print('TankDrive init called')
        super().__init__('TankDrive')
        self.debug = False
        self.logPrefix = "TankDrive: "

        # Speed controllers
        if robotmap.driveLine.speedControllerType == "VICTORSP":
            try:
                self.leftSpdCtrl = wpilib.VictorSP(robotmap.driveLine.leftMotorPort)
                if robotmap.driveLine.invertLeft:
                    self.leftSpdCtrl.setInverted(True)
            except Exception as e:
                print("{}Exception caught instantiating left speed controller. {}".format(self.logPrefix, e))
                if not wpilib.DriverStation.getInstance().isFmsAttached():
                    raise

            try:
                self.rightSpdCtrl = wpilib.VictorSP(robotmap.driveLine.rightMotorPort)
                if robotmap.driveLine.invertRight:
                    self.rightSpdCtrl.setInverted(True)
            except Exception as e:
                print("{}Exception caught instantiating right speed controller. {}".format(self.logPrefix, e))
                if not wpilib.DriverStation.getInstance().isFmsAttached():
                    raise
        elif robotmap.driveLine.speedControllerType == "TALON":
            try:
                self.leftSpdCtrl = wpilib.Talon(robotmap.driveLine.leftMotorPort)
                if robotmap.driveLine.invertLeft:
                    self.leftSpdCtrl.setInverted(True)
            except Exception as e:
                print("{}Exception caught instantiating left speed controller. {}".format(self.logPrefix, e))
                if not wpilib.DriverStation.getInstance().isFmsAttached():
                    raise

            try:
                self.rightSpdCtrl = wpilib.Talon(robotmap.driveLine.rightMotorPort)
                if robotmap.driveLine.invertRight:
                    self.rightSpdCtrl.setInverted(True)
            except Exception as e:
                print("{}Exception caught instantiating right speed controller. {}".format(self.logPrefix, e))
                if not wpilib.DriverStation.getInstance().isFmsAttached():
                    raise
        else:
            print("{}Configured speed controller type in robotmap not recognized - {}".format(self.logPrefix, robotmap.driveLine.speedControllerType))
            if not wpilib.DriverStation.getInstance().isFmsAttached():
                raise RuntimeError('Driveline speed controller specified in robotmap not valid: ' + robotmap.driveLine.speedControllerType)

        # Encoders
        try:
            self.leftEncoder = wpilib.Encoder(robotmap.driveLine.leftEncAPort, robotmap.driveLine.leftEncBPort,
                                              robotmap.driveLine.leftEncReverse, robotmap.driveLine.leftEncType)
            self.leftEncoder.setDistancePerPulse(robotmap.driveLine.inchesPerTick)
        except Exception as e:
            print("{}Exception caught instantiating left encoder. {}".format(self.logPrefix, e))
            if not  wpilib.DriverStation.getInstance().isFmsAttached():
                raise

        try:
            self.rightEncoder = wpilib.Encoder(robotmap.driveLine.rightEncAPort, robotmap.driveLine.rightEncBPort,
                                               robotmap.driveLine.rightEncReverse, robotmap.driveLine.rightEncType)
            self.rightEncoder.setDistancePerPulse(robotmap.driveLine.inchesPerTick)
        except Exception as e:
            print("{}Exception caught instantiating left encoder. {}".format(self.logPrefix, e))
            if not  wpilib.DriverStation.getInstance().isFmsAttached():
                raise

    # ------------------------------------------------------------------------------------------------------------------
    def initDefaultCommand(self):
        if robotmap.driveLine.controlStyle == "nfs":
            self.setDefaultCommand(DriveTeleopDefaultNFS())
            print("{}Default command set to DriveTeleopDefaultNFS".format(self.logPrefix))
        else:
            self.setDefaultCommand(DriveTeleopDefaultSkid())
            print("{}Default command set to DriveTeleopDefaultSkid".format(self.logPrefix))

    def driveRaw(self, left, right):
        if self.debug:
            if self.leftSpdCtrl:
                self.leftSpdCtrl.set(0.0)
            if self.rightSpdCtrl:
                self.rightSpdCtrl.set(0.0)
        else:
            if self.leftSpdCtrl:
                self.leftSpdCtrl.set(left)
            if self.rightSpdCtrl:
                self.rightSpdCtrl.set(right)

    def stop(self):
        if self.leftSpdCtrl:
            self.leftSpdCtrl.set(0.0)
        if self.rightSpdCtrl:
            self.rightSpdCtrl.set(0.0)

