import passwords
import mdParser
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

username = passwords.username
password = passwords.password

driver = webdriver.Firefox()

driver.get("https://asdk12.instructure.com/")

driver.find_element(By.ID, "userNameInput").send_keys(username)
password_box = driver.find_element(By.ID, "passwordInput")
password_box.send_keys(password)
password_box.send_keys(Keys.ENTER)

time.sleep(5)

cookiejson = driver.get_cookie("canvas_session")
cookie = {"name": cookiejson["name"], "value": cookiejson["value"]}
print(cookie)

content = requests.get("https://asdk12.instructure.com/", cookies=cookie).history

for page in content:
    print(page.url)
