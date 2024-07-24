from compartment import compartment
from command import command
from mdParser import markdown
from mdParser import excaped
import curses
import sys
import os
import cache

class cli(compartment):
    def __init__(self, x: int, y: int) -> None:
        self.screen = None
        self.template = "\n run anything:\n *=>* _{}_"
        self.command = ""
        self.currentDirectory = "/"
        width = 40
        height = 4
        self.displayed = self.command.ljust(width - 7, " ")
        super().__init__(int(x - width / 2), int(y - height / 2), width, height, 100, self.template.format(self.displayed))

        self.inverse = True 

        self.commands: list[command] = [
                command("q", lambda unused: exit()),
                command("wq", lambda unused: exit()),
                command("/", lambda directory: self.navTo(directory) ),
                command(".", lambda directory: self.navTo(self.currentDirectory + "/" + directory[1:])),
        ]

    def reset(self) -> None:
        self.command = ""
        self.update()

    def sendKey(self, key) -> None:
        if key == chr(127): # backspace
            self.command = self.command[:-1]
        elif key == chr(0x0D): # carrige feed, returned form the enter key
            self.run(self.command)
            self.command = ""
        else:
            self.command += key
        self.update()

    def run(self, command):
        for c in self.commands:
            if c.matches(command):
                c.toRun(command.replace(c.name + " ", "", 1))
                return
            

    def navTo(self, directory: str) -> None:
        path = directory.split("/")[1:]
        print(path)
        bestDirectory = ""
        for i in range(len(path)):
            maximum = -1
            bestName = ""
            for f in cache.cache.get(bestDirectory).files:
                print(f.name)
                dist = cache.fuzzyFind(f.name, path[i])
                print(dist)
                if(dist > maximum):
                    maximum = dist
                    bestName = f.name
            bestDirectory += bestName + "/"
        self.currentDirectory = bestDirectory.removesuffix("/")

    def update(self) -> None:
        start = max(len(self.command) - (self.width - 7), 0)

        self.displayed = self.command[start:].ljust(self.width - 7, " ")
        self.md = markdown(self.width, self.height, self.template.format(excaped(self.displayed)))

