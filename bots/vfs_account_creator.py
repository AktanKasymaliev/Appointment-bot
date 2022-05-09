from time import sleep
from typing import Any

from bots.bot_managing import Bot

from selenium.webdriver.common.by import By

class VFSAccountCreate(Bot):
    URL = "https://visa.vfsglobal.com/tur/en/pol/register"

    def __init__(self, email: str, password: str,  use_proxy: bool = False) -> None:
        super().__init__(use_proxy)
        self.email = email
        self.password = password

    def work(self) -> Any:
        data = {} # For collecting user credentials
        self.driver.get(self.URL)
        sleep(6)
        try:
            self.driver.find_element(By.ID, "mat-input-0").send_keys(self.email)
            sleep(2)
            self.driver.find_element(By.ID, "mat-input-1").send_keys(self.password)
            sleep(2)
            self.driver.find_element(By.ID, "mat-input-2").send_keys(self.password)
            sleep(2)

            self.driver.find_element(By.CLASS_NAME, 'mat-checkbox-layout').click()
            self.driver.find_element(By.CLASS_NAME, 'mat-btn-lg').click()
            sleep(3)
            self.generate_report(data)
            sleep(15)
            self.driver.close()
            print('=========Created VFS user!=========') 
        except:
            print("Failed while creating account...\nRetrying")
            self.work()
    
    def generate_report(self, data: dict) -> Any:
        return data