# Andrew Wang 2022
# 
# Is This Cheating?
# Auto-enters guesses into CS10A assessments to brute force crack answers
# Subverts copy-paste restriction
# 
# Credits: Tom Rebold, Monterey Peninsula College


import string

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def input_keys(xpath, keys):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.find_element(by=By.XPATH, value=xpath).send_keys(keys)


driver = webdriver.Chrome()
driver.get("https://tomrebold.com/csis10a/assess/13/")

input_keys('//*[@id="User"]', "WangAn" + Keys.ENTER)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "userAns[]")))
boxes = driver.find_elements(by=By.NAME, value="userAns[]")
checks = [driver.find_element(by=By.ID, value=f"Chk{i}") for i in range(1, len(boxes) + 1)]

# Question Number
i = 1  
# Guess string
guess = string.ascii_uppercase + string.ascii_lowercase * 10

boxes[i - 1].send_keys(guess)
checks[i - 1].click()

