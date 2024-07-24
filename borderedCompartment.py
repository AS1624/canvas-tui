from compartment import compartment
from output import *
import output
from mdParser import markdown

class borderedCompartment(compartment):
    def __init__(self, x: int, y: int, width: int, height: int, zIndex: float, text: str):
        super().__init__(x, y, width, height, zIndex, text)
        self.md: markdown = markdown(width - 2, height - 2, text)
        self.borderColor = self.color
        self.blockBorder = False

    def display(self) -> None:
        width = self.width
        height = self.height
        self.drawBorder()
        self.renderMD(width - 2 - self.blockBorder * 2, height - 2, self.x + 1 + self.blockBorder, self.y + 1)
    def drawBorder(self):
        x, y = (0, 0)
        width, height = (self.width, self.height)
        while y < height:
            if not self.blockBorder:
                char = ''
                if (
                           (x == 0         and y == 0)
                        or (x == 0         and y == height - 1)
                        or (x == width - 1 and y == 0)
                        or (x == width - 1 and y == height - 1)
                        ):
                    char = '+'
                elif y == 0 or y == height - 1:
                    char = "-"
                elif x == 0 or x == width - 1:
                    char = "|"

                if char != '':
                    putChar(x + self.x, y + self.y, char, bold = True, inverse = self.inverse, color = self.borderColor)
                    pass
            else:
                if x == 0 or x == 1 or x == width - 2 or x == width - 1 or y == 0 or y == height - 1:
                    putChar(x + self.x, y + self.y, " ", color = self.borderColor, inverse = True)
                    pass

            x += 1
            if x >= width:
                y += 1
                x = 0
