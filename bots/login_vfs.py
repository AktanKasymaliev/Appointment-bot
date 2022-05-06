from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

EMAIL = "aypztm.p.c.ov.dz.yl.qk.d@gmail.com"
PASSW = "Aktan@@1"

def monitor():

    driver = webdriver.Firefox(
        service=Service(executable_path="/home/aktan/projects/appointment-bot/geckodriver")
    )
    
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver

def login(driver, url):
    driver.get(url)
    driver.find_element(By.ID, 'mat-input-0').send_keys(EMAIL)
    driver.find_element(By.ID, 'mat-input-1').send_keys(PASSW)

    driver.find_element(By.CLASS_NAME, 'mat-btn-lg').click()


def main(url) -> None:
    r = monitor()
    login(r, url)

if __name__ == '__main__':
    URL = "https://visa.vfsglobal.com/tur/en/pol/login"
    main(URL)