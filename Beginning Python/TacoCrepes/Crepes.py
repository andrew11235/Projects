from selenium import webdriver

browser = webdriver.Chrome(executable_path='')
browser.get("https://forms.gle/1vHf6yFeHNGbCv4Q6")

for i in range(100):
  choice = browser.find_element_by_xpath("")
  submit = browser.find_element_by_xpath("")

  choice.click()
  submit.click()
  
  browser.refresh()
  
browser.close()
