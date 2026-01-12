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
#extractor = DigitalOut(brain.three_wire_port.a)

# DRIVE CODE
def drive():
    while(True):
        controller.screen.clear_row(0)
        vals = getDriveInput() #  gets input as an array
        controller.screen.print("L:", vals[0], " R:", vals[1])
        left_drive_smart.spin(FORWARD,vals[0],PERCENT) #  spins left side of the drivebase
        right_drive_smart.spin(FORWARD, vals[1], PERCENT) #  spins right side of the drivebase
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

# def extract():
#     extractor.set(False)
#     while True:
#         if(controller.buttonA.pressing()):
#             extractor.set(True)
#         elif(controller.buttonB.pressing()):
#             extractor.set(False)


# # INTAKE CODE
def intake():
    while(True):
        if(controller.buttonL2.pressing()): #checks if button is pressed
            intake_motor.spin(FORWARD, 100, PERCENT)
        elif(controller.buttonR2.pressing()):
            intake_motor.spin(REVERSE, 100, PERCENT)                              
        else:
            intake_motor.spin(FORWARD, 0, PERCENT)
        sleep(10, MSEC)

# initialisation function for driver control. while loops will be within the functions.
def usercontrol():
    Thread(drive)
    Thread(intake)

def autonomous():
    # Movementacros - no need to modify these
    MD_FORWARD = 1
    MD_LEFT = 2
    MD_RIGHT = 3
    MD_BACK= 4

    # --- MODIFY FROM HERE --- each direction in the movements array should have a corresponding movement time in movementLengths, therefore both arrays should be the same size

    movements = [MD_FORWARD, MD_BACK] # MD_FORWARD, MD_BACK, MD_LEFT, MD_RIGHT
    movementLengths = [2500, 1000] # in ms
    velocityPercent = 75.0 # does what it says on the tin

    # --- TO HERE ---
    for i in range(0, len(movements)):
        if(movements[i] == MD_FORWARD):
            left_drive_smart.spin(FORWARD, velocityPercent, PERCENT)
            right_drive_smart.spin(FORWARD, velocityPercent, PERCENT)
        if(movements[i] == MD_BACK):
            left_drive_smart.spin(REVERSE, velocityPercent, PERCENT)
            right_drive_smart.spin(REVERSE, velocityPercent, PERCENT)
        if(movements[i] == MD_LEFT):
            left_drive_smart.spin(REVERSE, 100 - velocityPercent, PERCENT)
            right_drive_smart.spin(FORWARD, velocityPercent, PERCENT)
        if(movements[i] == MD_RIGHT):
            left_drive_smart.spin(FORWARD, velocityPercent, PERCENT)
            right_drive_smart.spin(REVERSE, 100 - velocityPercent, PERCENT)
        sleep(movementLengths[i], TimeUnits.MSEC)
        left_drive_smart.stop()
        right_drive_smart.stop()

 
comp = Competition(usercontrol, autonomous)