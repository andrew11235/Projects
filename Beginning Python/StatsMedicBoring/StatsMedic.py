from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()


def wait_until_element(by, val):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, val)))


def wait_until_url(url):
    WebDriverWait(driver, 10).until(EC.url_matches(url))


def input_keys(xpath, keys):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.find_element(by=By.XPATH, value=xpath).send_keys(keys)


def reset_all():
    resets = driver.find_elements(by=By.CSS_SELECTOR,
                                  value="button[class='sc-kFCsca sc-hABAzo sc-fmKESZ gzmgat kXPsdr fzqZbg Button text medium rounded interactive']")
    for r in resets:
        r.click()


def submit_all():
    submits = driver.find_elements(by=By.CSS_SELECTOR, value="button[type='submit']")
    submits = submits[:len(submits) - 1]

    for s in submits:
        s.click()


def main():
    driver.get(r"https://review.statsmedic.com/auth/sign-in/")

    wait_until_element(By.CSS_SELECTOR, "#username")
    driver.find_element(by=By.CSS_SELECTOR, value="#username").send_keys("awang1@cusd.me")
    driver.find_element(by=By.CSS_SELECTOR, value="#password").send_keys("Andy4528" + Keys.ENTER)
    wait_until_url("https://review.statsmedic.com/home/learn/")

    driver.get(r"https://review.statsmedic.com/library/2023-stats-medic-ap-statistics-exam-review-course-194037/485079/path/step/224238048/")

    wait_until_element(By.CSS_SELECTOR, "input[type='radio']")

    radios = driver.find_elements(by=By.CSS_SELECTOR, value="input[type='radio']")
    radios_a = radios[::5]

    for r in radios_a:
        r.click()

    submit_all()

    fffs = driver.find_elements(by=By.CSS_SELECTOR, value="div[class='sc-izmEGP hlOxlZ']")
    feedbacks = []
    for i in range(len(fffs)):
        txt = fffs[i].find_element(by=By.CSS_SELECTOR, value="em[style='color: rgb(0, 0, 0);'], em:not([style])").text
        print(txt)
        feedbacks += txt[txt.rindex("(") + 1]

    print(len(feedbacks))

    l2n = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
    }

    reset_all()
    print(feedbacks)
    qn = 0
    for i in range(0, len(radios), 5):
        radios[i + l2n[feedbacks[qn]]].click()
        qn += 1

    submit_all()
    # driver.refresh()

    input()


if __name__ == '__main__':
    main()
