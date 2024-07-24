import os
import difflib
import api

class file:
    def __init__(self, name: str, text: str):
        self.name = name
        self.text = text

    def __str__(self) -> str:
        return self.name
    

class directory(file):
    def __init__(self, name: str, files: list[file], text: str):
        super().__init__(name, text)
        self.files = files

    def __str__(self) -> str:
        output = self.name
        if not (len(self.files) == 1 and self.files[0].name == "-.md"):
            for f in self.files:
                if str(f) != "":
                    output += ("\n" + str(f)).replace("\n", "\n    ")
            return output
        else:
            return ""

    def get(self, path: str) -> file:
        direc = path.split("/")[0]
        if direc.endswith(".md"):
            for f in self.files:
                if f.name == direc:
                    return f
            return None
        elif len(direc) == 0: return self
        else:
            for f in self.files:
                if f.name == direc:
                    return f.get(path.removeprefix(direc + "/"))
            return None
    

def elementsIn(direc: str) -> list[file]:
    files = os.listdir(direc)
    output = []
    for f in files:
        fullPath = ( direc + "/" + f ).replace(" ", r"\ ")
        if not f.endswith(".md"):

            with open(fullPath + "/-.md", "r") as text:
                output.append(directory(f, elementsIn(direc + "/" + f), text.read()))
        else:
            with open(fullPath, "r") as text:
                output.append(file(f), text.read())
    return output

def fuzzyFind(str1: str, str2: str) -> float:
    return difflib.SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    return 0

courses = api.loadCourses()
for course in courses:
    api.loadModules(course.get("id"))
    api.loadPages(course.get("id"))


cache: directory = directory("cache", elementsIn(".cache/pages"))
