import page
from borderedCompartment import borderedCompartment
from compartment import compartment
import output
import curses
import time
from mdParser import excaped
from mdParser import markdown
from screen import screen
from cli import cli
from math import floor
import cache

filesWidth = 40

def main(window: curses.window):
    width = output.width
    height = output.height

    focused = "screen"


    cliTab = cli(int(width / 2), int(height / 2))

    dirTab = compartment(0, 0, width, 1, 1, "")
    dirTab.color = 1

    files = ""
    for f in cache.cache.files:
        files += str(f) + "\n\n=—==========================\n\n"
    filesTab = borderedCompartment(0, 1, filesWidth, height - 1, 0, excaped(files))
    filesTab.borderColor = 2
    filesTab.blockBorder = True

    mainTab = compartment(filesWidth, 1, width - filesWidth, height - 1, 0, "")

    scr = screen([dirTab, filesTab])

    cliTab.screen = scr
    
    while(True):
        dirTab.md.parse('*_' + excaped(cliTab.currentDirectory))
        mainTab.md.parse(cache.cache.get(cliTab.currentDirectory).text)
        scr.display()

        value = output.readBuffer()
        if value == "":
            exit(0)

        if focused == "screen":
            if value == ':' or value == ";":
                scr.add(cliTab)
                focused = "cli"
            elif value == '/' or value == '.':
                scr.add(cliTab)
                focused = "cli"
                cliTab.command = value
                cliTab.update()
        elif focused == "cli":
            if value == chr(0x1b): # escape
                scr.remove(cliTab)
                cliTab.reset()
                focused = "screen"
            elif value == chr(0x0D): # enter
                cliTab.sendKey(value)
                scr.remove(cliTab)
                cliTab.reset()
                focused = "screen"
            elif len(value) != 0:
                cliTab.sendKey(value)


output.init(main)
