from compartment import compartment
import output

class screen:
    def __init__(self, compartments: list[compartment]):
        self.compartments = compartments
        self.compartments.sort(key = lambda it: it.zIndex)

    def display(self, compartments: list[compartment] = []) -> None:
        output.clear()

        for it in self.compartments:
            it.display()

        compartments.sort(key = lambda it: it.zIndex)
        for it in compartments:
            it.display()

    def add(self, compartment: compartment):
        self.compartments.append(compartment)

    def remove(self, compartment: compartment) -> bool:
        try:
            self.compartments.remove(compartment)
        except:
            return False
        finally:
            return True

if __name__ == "__main__":
    test = screen([
        compartment(0, 0, 2, 3, 10, "jfkdsla"),
        compartment(1, 1, 5, 6, 1, "irenfl")
        ])
    print(test.compartments)
