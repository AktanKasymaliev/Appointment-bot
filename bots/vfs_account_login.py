from time import sleep

from selenium.webdriver.common.by import By

from bots.bot_managing import Bot


class VFSLoginBot(Bot):

    URL = "https://visa.vfsglobal.com/tur/en/pol/login"

    def __init__(self, email: str, password: str, use_proxy: bool = True,) -> None:
        self.driver = self.create_driver(use_proxy)
        self.email = email
        self.password = password


    def work(self):
        self.driver.get(self.url)
        sleep(4)
        try:
            self.driver.find_element(By.ID, 'mat-input-0').send_keys(self.email)
            sleep(2)
            self.driver.find_element(By.ID, 'mat-input-1').send_keys(self.password)
            sleep(2)
            self.driver.find_element(By.CLASS_NAME, 'mat-btn-lg').click()
        except:
            print("Email or password was given incorrect!")