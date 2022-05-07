from time import sleep
from typing import Any

import undetected_chromedriver as uc
from bots.bot_managing import AbstractBot, Proxies

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class VFSAccountCreate(AbstractBot):
    URL = "https://visa.vfsglobal.com/tur/en/pol/register"

    def __init__(self, use_proxy: bool = False) -> None:
        self.driver = self.__open_browser(use_proxy)

    def work(self) -> Any:
        data = {} # For collecting user credentials
        self.driver.get(self.URL)
        print("Creating User")
        try:
            self.driver.find_element(By.ID, "mat-input-0").send_keys("outlook@outlook.com")
            sleep(1)
            self.driver.find_element(By.ID, "mat-input-1").send_keys("password1")
            sleep(1)
            self.driver.find_element(By.ID, "mat-input-2").send_keys("password1")
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

    @staticmethod
    def __open_browser(use_proxy: bool = False) -> uc.Chrome:
        options = uc.ChromeOptions()
        if use_proxy:
            plugin_file = Proxies.make_proxy()
            options.add_extension(plugin_file)

        options.add_argument("--disable-web-security")
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument("--disable-application-cache")

        driver = uc.Chrome(
            options=options,
            service=Service(ChromeDriverManager().install())
        )

        driver.maximize_window()
        driver.implicitly_wait(10)
        return driver