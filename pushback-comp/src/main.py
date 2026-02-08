# Library imports
from vex import *

brain = Brain()
controller = Controller()
# drivebase
right_drive_back = Motor(Ports.PORT20, True) #TODO fix, free spin
right_drive_middle = Motor(Ports.PORT12, True)
right_drive_front = Motor(Ports.PORT11, True)
left_drive_back = Motor(Ports.PORT2) #dead
left_drive_middle = Motor(Ports.PORT13) #TODO fix, spun freely
left_drive_front = Motor(Ports.PORT1)
left_drive_smart = MotorGroup(left_drive_back, left_drive_middle, left_drive_front)
right_drive_smart = MotorGroup(right_drive_back, right_drive_middle, right_drive_front)
drivetrain = MotorGroup(left_drive_smart, right_drive_smart)
# intake/lift
intake_motor = Motor(Ports.PORT10, True)
outtake_motor = Motor(Ports.PORT12, True) # TODO set motor number

extractor = DigitalOut(brain.three_wire_port.a)

# DRIVE CODE
def drive():
    while(True):
        controller.screen.clear_row(0)
        vals = getDriveInput() #  gets input as an array
        controller.screen.print("L:", vals[0], " R:", vals[1])
        right_drive_smart.spin(FORWARD,vals[0],PERCENT) #  spins left side of the drivebase
        left_drive_smart.spin(FORWARD, vals[1], PERCENT) #  spins right side of the drivebase
        sleep(10, MSEC)

# process input from sticks 
def getDriveInput():
    vals = [controller.axis3.value(), controller.axis2.value()] # axis3 gets left input, axis2 gets right input
    for i in vals: # goes through the vals array, converts values through the log algorithms
        if(i > 0):
            i = (2**(i*(math.log(100)/math.log(2))/127))
        elif(i < 0):
            i = i*-1
            i = (2**(i*(math.log(100)/math.log(2))/127))
            i = i *-1
    return vals

def extract():
    extractor.set(False)
    while True:
        if(controller.buttonA.pressing()):
            extractor.set(True)
        elif(controller.buttonB.pressing()):
            extractor.set(False)


# # INTAKE CODE
def intake():
    while(True):
        if(controller.buttonL2.pressing()): #checks if button is pressed
            intake_motor.spin(FORWARD, 100, PERCENT)
        elif(controller.buttonR2.pressing()):
            intake_motor.spin(REVERSE, 70, PERCENT)                              
        else:
            intake_motor.spin(FORWARD, 0, PERCENT)
        sleep(10, MSEC)
    
def outtake():
    while(True):
        if(controller.buttonL1.pressing()): #checks if button is pressed
            outtake_motor.spin(FORWARD, 100, PERCENT)
        elif(controller.buttonR1.pressing()):
            outtake_motor.spin(REVERSE, 100, PERCENT)                              
        else:
            outtake_motor.spin(FORWARD, 0, PERCENT)
        sleep(10, MSEC)

# initialisation function for driver control. while loops will be within the functions.
def usercontrol():
    Thread(drive)
    Thread(intake)
    Thread(outtake)
    Thread(extract)

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

    movements = [MD_EXTRACTORDOWN, MD_FORWARD] # MD_FORWARD, MD_BACK, MD_LEFT, MD_RIGHT
    movementLengths = [1, 1500] # in ms
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
    


 
comp = Competition(usercontrol, autonomous)