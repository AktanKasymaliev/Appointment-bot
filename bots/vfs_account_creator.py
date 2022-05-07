from time import sleep
from typing import Any

import undetected_chromedriver as uc
from bots.bot_managing import Bot, Proxies

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class VFSAccountCreate(Bot):
    URL = "https://visa.vfsglobal.com/tur/en/pol/register"

    def __init__(self, email: str, password: str, use_proxy: bool = False) -> None:
        self.email = email
        self.password = password
        self.driver = self.create_driver(use_proxy)

    def work(self) -> Any:
        data = {} # For collecting user credentials
        self.driver.get(self.URL)
        print("Creating User")
        try:
            self.driver.find_element(By.ID, "mat-input-0").send_keys(self.email)
            sleep(1)
            self.driver.find_element(By.ID, "mat-input-1").send_keys(self.password)
            sleep(1)
            self.driver.find_element(By.ID, "mat-input-2").send_keys(self.password)
            sleep(1)

            self.driver.find_element(By.CLASS_NAME, 'mat-checkbox-layout').click()
            self.driver.find_element(By.CLASS_NAME, 'mat-btn-lg').click()
            sleep(2)
            self.generate_report(data)
        except:
            print("Failed while creating account...\nRetrying")
            self.work()
    
    def generate_report(self, data: dict) -> Any:
        return data