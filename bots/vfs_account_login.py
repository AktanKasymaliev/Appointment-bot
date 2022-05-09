from time import sleep
from typing import Any

from selenium.webdriver.common.by import By

from bots.bot_managing import Bot


class VFSLoginBot(Bot):

    URL = "https://visa.vfsglobal.com/tur/en/pol/login"

    def __init__(self, email: str, password: str,  use_proxy: bool = False) -> None:
        super().__init__(use_proxy)
        self.email = email
        self.password = password


    def work(self):
        self.driver.get(self.URL)
        sleep(10)
        try:
            self.driver.find_element(By.ID, 'mat-input-0').send_keys(self.email)
            sleep(2)
            self.driver.find_element(By.ID, 'mat-input-1').send_keys(self.password)
            sleep(2)
            self.driver.find_element(By.CLASS_NAME, 'mat-btn-lg').click()
            sleep(10)
        except:
            print("Email or password was given incorrect!")

    def generate_report(self) -> Any:
        return super().generate_report()