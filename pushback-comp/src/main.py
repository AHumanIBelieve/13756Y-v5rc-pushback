# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Chaitya Jain                                                 #
# 	Created:      9/22/2025, 4:13:08 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

brain = Brain()
controller = Controller()
# drivebase
right_drive_back = Motor(Ports.PORT10)
right_drive_front = Motor(Ports.PORT9, True)
left_drive_back = Motor(Ports.PORT1)
left_drive_front = Motor(Ports.PORT20, True)
left_drive_smart = MotorGroup(left_drive_back, left_drive_front)
right_drive_smart = MotorGroup(right_drive_back, right_drive_front)
drivetrain = MotorGroup(left_drive_smart, right_drive_smart)
# intake/lift
#intake_motor = Motor(Ports.PORT18)
extractor = DigitalOut(brain.three_wire_port.a)

# DRIVE CODE
def drive():
    while(True):
        controller.screen.clear_row(0)
        vals = getDriveInput() #  gets input as an array
        controller.screen.print("L:", vals[0], " R:", vals[1])
        left_drive_smart.spin(FORWARD,vals[0],PERCENT) #  spins left side of the drivebase
        right_drive_smart.spin(REVERSE, vals[1], PERCENT) #  spins right side of the drivebase
        sleep(10, MSEC)

# process input from sticks 
def getDriveInput():
    vals = [controller.axis3.value(), controller.axis2.value()] # axis3 gets left input, axis2 gets right input
    for i in vals: # goes through the vals array, checks if -10<value<10, and if it is, sets it to 0
        if(i > 0):
            i = (2**(i*(math.log(100)/math.log(2))/127))
        elif(i < 0):
            i = i*-1
            i = (2**(i*(math.log(100)/math.log(2))/127))
            i = i *-1
    return vals

# # INTAKE CODE
# intake_forward = False
# intake_reverse = False
# def intake():
#     global intake_forward, intake_reverse, intake_motor
#     while(True):
#         if(controller.buttonL2.pressing()): #checks if button is pressed
#             intake_motor.spin(FORWARD, 100, PERCENT)
#         elif(controller.buttonR2.pressing()):
#             intake_motor.spin(REVERSE, 100, PERCENT)
#         else:
#             intake_motor.spin(FORWARD, 0, PERCENT)
#         sleep(10, MSEC)

# LIFT CODE
#lift_forward = False
#left_reverse = False
#banana = Motor(Ports.PORT5, True)
#smartbanana = (banana)
# def lift():
#     global lift_forward, lift_reverse, lift_motor
#     while(True):
#         if(controller.buttonL1.pressing()): #checks if button is pressed
#             banana.spin(FORWARD, 100, PERCENT)
#         elif(controller.buttonR1.pressing()):
#             banana.spin(REVERSE, 100, PERCENT)
#         else:
#             banana.spin(FORWARD, 0, PERCENT)
#         sleep(10, MSEC)

def extract():
    extractor.set(False)
    while True:
        if(controller.buttonA.pressing()):
            extractor.set(True)
        elif(controller.buttonB.pressing()):
            extractor.set(False)

def autonomous():
    controller.screen.print("brrrrrrrrr")

# initialisation function for driver control. while loops will be within the functions.
def usercontrol():
    Thread(drive)
    Thread(extract)
 
comp = Competition(usercontrol, autonomous)