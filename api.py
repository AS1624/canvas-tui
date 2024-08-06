import requests
import passwords
import json
import re
import os
import mdParser

ftcCourseId = "3947~292126"

def load(path: str, *params: str) -> json:
    url = "https://canvas.instructure.com/api/v1/{}?access_token={}".format(path, passwords.token)
    for param in params:
        url += "&&" + param
    print(url)
    response = requests.get(url)
    if response.status_code != 200:
        return "failed"
    else:
        return response.json()

def loadOrUseCached(path: str, *params: str) -> json:
    fileName = ".cache/api/" + path + "/-"
    if os.path.exists(fileName):
        with open(fileName, "r") as file:
            value = file.read()
            return json.loads(value)
    else:
        return load(path, *params)
def save(path: str, output: any, meta: str = "") -> None:
    path = ".cache/api/" + path + "/-"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    value = json.dumps(output).replace("None", "null")

    with open(path, "w") as file:
        file.write(value)
    with open(path + ".meta", "w") as file:
        file.write(meta)

def savePage(path: str, md: str) -> None:
    path = ".cache/pages/" + path + "/-.md"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    value = md

    with open(path, "w") as file:
        file.write(value)

    
def loadCourses() -> dict:
    value = loadOrUseCached("courses")
    if value == "failed":
        return []
    output = []
    for i in range(len(value)):
        output.append({"name": value[i].get('name'), "id": value[i].get('id')})
    save("courses", output)
    savePage(value[i].get('name'), "") # TODO: fill out
    return output
def loadModules(course: str) -> list[list[str]]:
    url = "courses/{}/modules".format(course)

    value = loadOrUseCached(url, "include[]=items")
    if value == "failed":
        return []
    output = []
    for i in range(len(value)):
        output.append(
                {
                    "name": value[i].get("name"),
                    "items": []
                }
        )
        for item in value[i].get("items"):
            output[i]["items"].append(
                {
                    "title": str(item.get("title")).replace("\"", "'"),
                    "url": str(item.get("url")).replace("https://canvas.instructure.com/api/v1/", "")
                }
            )
    save(url, output)
    return output
def loadItems(course: str):
    modules = loadModules(course)
    output = []
    for module in modules:
        output.append({"name": module.get("name"), "assignments": []})
        for item in module.get("items"):
            if item.get("url") != None:
                url = str(item.get("url")).replace("https://canvas.instructure.com/api/v1/", "")
                if url != "None" and url != "null":
                    assignment = loadOrUseCached(url)
                    if assignment != "failed":
                        result = {
                                "description": str(assignment.get("description")).replace("'", "\""),
                                "locked_for_user": assignment.get("locked_for_user"),
                                "html_url": assignment.get("html_url"),
                                "name": assignment.get("name")
                        }
                        output[-1].get("assignments").append(result)
                        save(url, result)
    return output
def loadPages(course: str):
    modules = loadItems(course)
    output = []
    for module in modules:
        for item in module.get("assignments"):
            description = item.get("description")

            if description != None and description != "null" and description != "None":
                courseName = next(
                                filter(
                                    lambda d: d.get("id") == course,
                                    loadOrUseCached("courses")
                                    )
                            ).get("name")
                
                url = "{}/{}/{}".format(courseName, module.get("name"), item.get("name"))
                savePage(url, mdParser.parseHTML(description))

    return output


