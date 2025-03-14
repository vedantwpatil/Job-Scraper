from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Safari()

driver.get("https://www.espn.com/")

try:
    element = driver.find_element(By.CSS_SELECTOR, ".shoes")
    print(element.text)
except:
    pass

driver.quit()
print("Finished")
