
class command:
    def __init__(self, name: str, toRun: callable):
        self.name = name
        self.toRun = toRun

    def matches(self, other: str) -> bool:
        if other.find(self.name) == 0:
            return True
        else:
            return False
