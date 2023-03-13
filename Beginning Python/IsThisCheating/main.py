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


def input_keys(driver, xpath, keys):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.find_element(by=By.XPATH, value=xpath).send_keys(keys)


def main():
    ab = input("10 A or B? <a/b>\n")
    drill_num = input("Drill #?\n")

    if len(drill_num) < 2:
        drill_num = "0" + drill_num

    driver = webdriver.Chrome()
    driver.get(f"https://tomrebold.com/csis10{ab}/assess/{drill_num}/")  # Assessment URL

    pw = input("Password?\n")

    input_keys(driver, '//*[@id="User"]', pw + Keys.ENTER)

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

        while True:
            ans = driver.find_element(by=By.CSS_SELECTOR, value=f"#feedback{i}").text
            if "#" in ans:
                break
            else:
                time.sleep(.005)

        ans = ans.replace('#', '')
        input_ans = ans[ans.index(')') + 1:ans.rindex('|') - 1]

        print(f"{i}: {input_ans}")

        boxes[i - 1].clear()
        boxes[i - 1].send_keys(input_ans)
        checks[i - 1].click()

        submits[i + 1].click()

    input()


if __name__ == '__main__':
    main()
