# Library imports
from vex import *

brain = Brain()
controller = Controller()

#declare all variables here

#drive code

def drive():
    #this will be the main driving loop, running the entire time
    while(True):
        #get controller input
        #translate input to wheels output
        #spin them wheels
        sleep(1) #TODO remove, placeholder to avoid syntax errors  
  
def intake():
    #this loop will also be running the entire time
    while(True):
        #if trigger 1 is pressed, go forward
        #if trigger 2 is pressed, go backwards
        #else go zero
        sleep(1) #TODO remove, placeholder to avoid syntax errors 
  
def usercontrol():
    Thread(drive)
    Thread(intake)