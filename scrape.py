import requests

sesh = requests.Session()
canvasCookie = sesh.get("https://asdk12.instructure.com/").history[0].cookies
sesh.get("https://adfs.asdk12.org/adfs/ls/", headers={"UserName": secrets.username, "Password": secrets.Password})

print(history[0].cookies)
