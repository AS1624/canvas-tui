import time
import sys
import output
from  mdParser import markdown
from borderedCompartment import borderedCompartment

def printLn(str):
    print(str, end="")
while(True):
    char = output.readBuffer()
    print(output.charCode(char))
