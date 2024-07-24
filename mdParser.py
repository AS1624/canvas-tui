import output
import re

specialChars = ['*', '_', '/', '-', '\\']

def excaped(string: str) -> str:
    output = ""
    for char in string:
        if char in specialChars:
            output += "\\"
        elif not char.isascii():
            char = ""
        output += char
    return output
def parseHTML(html: str) -> str:
    html = excaped(html)

    headerTag = re.compile(r"</?h[1-6]>")
    anyTag = re.compile(r"</?.+?>")
    html = headerTag.sub("-", html)
    html = anyTag.sub("", html)
    
    return html

class markdown:
    def __init__(self, width: int, height: int, text: str):
        self.width = width
        self.height = height

        self.parse(text)

    def parse(self, text) -> None:
        self.text: list[str] = [""] 
        self.bToggles = []
        self.iToggles = []
        self.uToggles = []
        self.hToggles = []

        height = self.height
        width = self.width

        excaped = False

        while(len(text) > 0):
            currentPos = (len(self.text[-1]), len(self.text) - 1)

            char = text[0]
            if char ==  '*' and not excaped:
                self.bToggles.append(currentPos)
                text = text[1:]
            elif char == '_' and not excaped:
                self.uToggles.append(currentPos)
                text = text[1:]
            elif char == '/' and not excaped:
                self.iToggles.append(currentPos)
                text = text[1:]
            elif char == '-' and not excaped:
                self.hToggles.append(currentPos)
                text = text[1:]
            elif char == chr(0x0A): # line feed
                self.text[-1] = self.text[-1].ljust(width)
                self.text.append("")
                text = text[1:]
            elif char == '\\':
                excaped = True
                text = text[1:]
            elif len(text[-1]) >= width:
                self.text.append("")
            else:
                self.text[-1] += char
                text = text[1:]
                excaped = False

        self.text[-1] = self.text[-1].ljust(width, " ")
        for i in range(height - len(self.text)):
            self.text.append("".ljust(width))


