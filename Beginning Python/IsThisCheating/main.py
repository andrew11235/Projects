# Andrew Wang 2023
#
# Is This Cheating...?
#
# Auto-enters guesses into CS10 assessments to brute force answers
# Subverts copy-paste restriction
#
# Credit: Tom Rebold, Monterey Peninsula College

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def input_keys(xpath, keys):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.find_element(by=By.XPATH, value=xpath).send_keys(keys)


driver = webdriver.Chrome()
driver.get("https://tomrebold.com/csis10b/assess/12/")  # Assessment URL

pw = input("Password?\n")

input_keys('//*[@id="User"]', pw + Keys.ENTER)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "userAns[]")))
boxes = driver.find_elements(by=By.NAME, value="userAns[]")
checks = [driver.find_element(by=By.ID, value=f"Chk{i}") for i in range(1, len(boxes) + 1)]
submits = driver.find_elements(by=By.NAME, value="SubmitButton")

printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '

# Question Number
for i in range(1, len(boxes) + 1):

    guess = printable * len(driver.find_element(by=By.CSS_SELECTOR, value=f"#feedback{i}").text)

    boxes[i - 1].send_keys(guess)
    checks[i - 1].click()
    submits[i + 1].click()

    ans = driver.find_element(by=By.CSS_SELECTOR, value=f"#feedback{i}").text

    while True:
        ans = driver.find_element(by=By.CSS_SELECTOR, value=f"#feedback{i}").text
        if "#" in ans:
            break
        else:
            time.sleep(.005)

    ans = ans.replace('#', '')
    inputAns = ans[ans.index(')') + 1:ans.rindex('|') - 1]

    print(f"{i}: {inputAns}")

    boxes[i - 1].clear()
    boxes[i - 1].send_keys(inputAns)
    checks[i - 1].click()

    submits[i + 1].click()

input()
