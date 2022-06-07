import string

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def input_keys(xpath, keys):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.find_element(by=By.XPATH, value=xpath).send_keys(keys)


def input_click(xpath, keys):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.find_element(by=By.XPATH, value=xpath).click()


driver = webdriver.Chrome()
driver.get("https://tomrebold.com/csis10a/assess/13/")

input_keys('//*[@id="User"]', "WangAn" + Keys.ENTER)

guess = string.ascii_uppercase + string.ascii_lowercase * 10

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "userAns[]")))
boxes = driver.find_elements(by=By.NAME, value="userAns[]")
checks = [driver.find_element(by=By.ID, value=f"Chk{i}") for i in range(1, len(boxes) + 1)]
submits = driver.find_elements(by=By.NAME, value="SubmitButton")
submits.pop(0)

# for b in boxes:
#     b.send_keys(guess)

i = 1
boxes[i - 1].send_keys(guess)
checks[i - 1].click()




