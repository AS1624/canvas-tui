import output
from mdParser import markdown

class compartment:
    def __init__(self, x: int, y: int, width: int, height: int, zIndex: float, text: str):
        self.inverse = False
        self.color = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.zIndex = zIndex
        self.md: markdown = markdown(width, height, text)

    def display(self) -> None:
        width = self.width
        height = self.height
        self.renderMD(width, height, self.x, self.y)
        
    def renderMD(self, width: int, height: int, startX: int, startY: int):
        x = 0
        y = 0
        bold = False
        italics = False
        underline = False
        header = False
        while y < height:
            if (x, y) in self.md.bToggles:
                bold = not bold
            if (x, y) in self.md.iToggles:
                italics = not italics
            if (x, y) in self.md.uToggles:
                underline = not underline
            if (x, y) in self.md.hToggles:
                header = not header

            if x >= width:
                y += 1
                x = 0
            else:
                c = self.md.text[y][x]
                if header:
                    c = c.upper()
                output.putChar(x + startX, y + startY, c, bold, italics, underline, header, self.inverse, self.color)
                x += 1


