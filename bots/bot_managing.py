import os
from abc import ABC, abstractmethod
from typing import Any
from configparser import ConfigParser

import fake_useragent

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from selenium_stealth import stealth

from bots.constants import manifest_json, background_js
from bots.bot_configurations import  load_conf

class Proxie:

    def __init__(self, username: str, password: str, host: str, port: int) -> None:
        self.USERNAME = username
        self.PASSWORD = password
        self.HOST = host
        self.PORT = port 

    def give_the_path(self) -> str:
        return os.getcwd() + '/bots/proxy/'

    def make_proxy(self) -> None:
        path = self.give_the_path()

        with open(path + 'background.js', 'w') as f:
            f.write(background_js % (
                self.HOST, self.PORT, 
                self.USERNAME, self.PASSWORD
                    )
                )

        with open(path + 'manifest.json', 'w') as f:
            f.write(manifest_json)


class Bot(ABC):
    CONFIG_PARSE = ConfigParser()
    CONFIG_PARSE.read("bot_settings.ini")
    PROXY = "PROXY"

    USERNAME = load_conf(CONFIG_PARSE, PROXY, "PROXY_USERNAME")
    PASSWORD = load_conf(CONFIG_PARSE, PROXY, "PROXY_PASSWORD")
    HOST = load_conf(CONFIG_PARSE, PROXY, "PROXY_HOST")
    PORT = int(load_conf(CONFIG_PARSE, PROXY, "PROXY_PORT"))

    def __init__(self, use_proxy: bool = False) -> None:
        self.driver = self.create_driver(use_proxy)

    @abstractmethod
    def work(self) -> Any: 
        """
        Main method for start worker of this bot
        """
        pass

    @abstractmethod
    def generate_report(self) -> Any:
        """
        Method that returns final conclusion of work
        """ 
        pass
    
    def create_driver(self, use_proxy: bool = False) -> uc.Chrome:
        """
        Method for open your chrome browser
        """
        options = uc.ChromeOptions()
        if use_proxy:
            proxy = Proxie(
                self.USERNAME, self.PASSWORD,
                self.HOST, self.PORT
                )
            proxy.make_proxy()
            options.add_argument('--load-extension={}'.format(proxy.give_the_path()))
        options.add_argument("--headless")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument("--disable-application-cache")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.set_capability('useAutomationExtension', False)
        options.set_capability("excludeSwitches", ["enable-automation"])
        options.add_argument(f"user-agent={fake_useragent.UserAgent().random}")
        
        driver_path = ChromeDriverManager(path='/tmp').install()
        driver = uc.Chrome(
            service=Service(driver_path),
            options=options)

        # Make your driver more secretive
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
    
        driver.maximize_window()
        driver.implicitly_wait(10)

        return driver