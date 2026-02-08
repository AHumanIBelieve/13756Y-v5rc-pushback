# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Created:      2/8/2026, 7:54:21 AM                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

brain = Brain()
controller = Controller()
# drivebase
right_drive_back = Motor(Ports.PORT20) #TODO fix, free spin
right_drive_middle = Motor(Ports.PORT12)
right_drive_front = Motor(Ports.PORT11)
left_drive_back = Motor(Ports.PORT2, True) #dead
left_drive_middle = Motor(Ports.PORT13, True) #TODO fix, spun freely
left_drive_front = Motor(Ports.PORT1, True)
left_drive_smart = MotorGroup(left_drive_back, left_drive_middle, left_drive_front)
right_drive_smart = MotorGroup(right_drive_back, right_drive_middle, right_drive_front)
drivetrain = MotorGroup(left_drive_smart, right_drive_smart)
# intake/lift
intake_motor = Motor(Ports.PORT10, True)
outtake_motor = Motor(None, True) # TODO set motor number

extractor = DigitalOut(brain.three_wire_port.a)

def autonomous():
    # Movement macros - no need to modify these
    MD_FORWARD = 1
    MD_LEFT = 2
    MD_RIGHT = 3
    MD_BACK= 4
    MD_STARTINLIFT = 5
    MD_STARTOUTLIFT = 8
    MD_STOPLIFT = 9
    MD_STARTOUT = 10
    MD_STOPOUT = 11
    MD_PAUSE = 12
    MD_EXTRACTORDOWN = 13
    MD_EXTRACTUP = 14
    # --- MODIFY FROM HERE --- each direction in the movements array should have a corresponding movement time in movementLengths, therefore both arrays should be the same size
    movements = [MD_STARTINLIFT]
    movementLengths = [100]
    #movements = [MD_EXTRACTUP, MD_STARTINLIFT, MD_FORWARD, MD_EXTRACTORDOWN, MD_FORWARD, MD_PAUSE, MD_BACK] # MD_FORWARD, MD_BACK, MD_LEFT, MD_RIGHT
    #movementLengths = [1, 1, 1500, 1, 1500, 15000, 1500] # in ms
    velocityPercent = 75.0 # does what it says on the tin
    outVelocity = 100.0
    inVelocity = 70.0
    # --- TO HERE ---
    for i in range(0, len(movements)):
        if(movements[i] == MD_FORWARD):
            left_drive_smart.spin(FORWARD, velocityPercent, PERCENT)
            right_drive_smart.spin(FORWARD, velocityPercent, PERCENT)
        elif(movements[i] == MD_BACK):
            left_drive_smart.spin(REVERSE, velocityPercent, PERCENT)
            right_drive_smart.spin(REVERSE, velocityPercent, PERCENT)
        elif(movements[i] == MD_LEFT):
            left_drive_smart.spin(REVERSE, 100 - velocityPercent, PERCENT)
            right_drive_smart.spin(FORWARD, velocityPercent, PERCENT)
        elif(movements[i] == MD_RIGHT):
            left_drive_smart.spin(FORWARD, velocityPercent, PERCENT)
            right_drive_smart.spin(REVERSE, 100 - velocityPercent, PERCENT)
        elif(movements[i] == MD_STARTOUT):
            outtake_motor.spin(FORWARD, outVelocity, PERCENT)
        elif(movements[i] == MD_STOPOUT):
            outtake_motor.stop()
        elif(movements[i] == MD_STARTINLIFT):
            outtake_motor.spin(FORWARD, inVelocity, PERCENT)
        elif(movements[i] == MD_STARTOUTLIFT):
            outtake_motor.spin(REVERSE, inVelocity, PERCENT)
        elif(movements[i] == MD_STOPLIFT):
            intake_motor.stop()
        elif(movements[i] == MD_EXTRACTORDOWN):
            extractor.set(True)
        elif(movements[i] == MD_EXTRACTUP):
            extractor.set(False)
        sleep(movementLengths[i], TimeUnits.MSEC)
        left_drive_smart.stop()
        right_drive_smart.stop()

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place driver control in this while loop
    while True:
        wait(20, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()