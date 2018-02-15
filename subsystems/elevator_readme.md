The elevator system is in three sections
- immobile first section providin motor and rails to move second section
- second sections that is within first section, and provides motor and rails to move final section
- Final section to which the harvester mounts to (does not have any actuators or sensors of it's own)

The challenge with controlling this is the weight of sections back driving and falling down due to weight.
Motor power will have to be applied to maintain height of the crate/harvester at any given moment



We will create the code in three phases
1. Simplistic approach that allows driving up and down until the limit switches at each extent are reached
    - all height maintenance must be performed solely by the driver

2. Improved version that has a "holding speed" specified to adjust the speed up and down to keep the harvester more
stable with less effort

3. Using PID loop
PID loop will be displacement based using the analog signal that will indicate the overall height of the harvester
    - the driver will use the controller to adjust the setpoint rather than the speed directly

Movement rules
To maintain stability, and consistent operation, the following rules must be observed when moving the assemblies

Stage 2 should be given priority when moving up
Stage 1 should be giving priority when moving down

Allowed Movement Table:

                    S1 Bottom   S1 Top      S2 Bottom   S2 Top
S1 Drive Up:                    False                   True
S1 Drive Down:      False
S2 Drive Up:                                            False
S2 Drive Down:      True                    False

Example:
 S1 can only drive s2 up when the harvester is all the way at the top of S2, and S1 is not at it's top
 If the harvester is not at the top, that should move upwards first

 Conversely, if the S2 is not all the way down within S1, and a down movement is given, S1 should be driven to move S2
 down before starting to move the harvester down



Update:
The #2 method, just using a holding speed works fine.  No PID loop required, yay!