from time import sleep
from typing import Any

from selenium.webdriver.common.by import By

from bots.bot_managing import Bot

class OutlookCheckerMailBot(Bot):

    def __init__(self, email: str, password: str,  use_proxy: bool = False) -> None:
        super().__init__(use_proxy)
        self.email = email
        self.password = password

    def login(self):
        """
        Method which will sign in to outlook mail
        with you are given credentials
        """
        self.driver.get('https://outlook.office.com/mail/')
        sleep(4)
        try:
            self.driver.find_element(By.ID, 'i0116').send_keys(self.email)
            sleep(2)
            self.driver.find_element(By.ID, 'idSIButton9').click()
            sleep(2)
            self.driver.find_element(By.ID, 'i0118').send_keys(self.password)
            sleep(2)
            self.driver.find_element(By.ID, 'idSIButton9').click()
            sleep(3)
            self.driver.find_element(By.ID, 'idBtn_Back').click()
            sleep(5)
        except:
            print("Email or password was given incorrect!")

    def choose_vfs_verification_mail_and_click(self):
        try:
            self.driver.find_element(By.XPATH, "//span[text()='Other']").click()
            sleep(2)
            self.driver.find_element(By.XPATH, "//span[text()='donotreply@vfsglobal.com']").click()
            sleep(2)
            self.driver.find_element(By.XPATH, "//a[text()='ActivateAccount']").click()
            sleep(2)
            self.driver.close()
        except:
            print('The mail from VFS wasn\'t found!')

    def work(self):
        self.login()
        self.choose_vfs_verification_mail_and_click()
    
    def generate_report(self) -> Any:
        return super().generate_report()