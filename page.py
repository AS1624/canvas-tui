import output

class page:

    def __init__(self, text: str):
        self.text = text

    def display(self):
        output.clear()
        output.printText(self.text)
