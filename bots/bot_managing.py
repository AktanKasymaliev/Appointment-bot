import os
from abc import ABC, abstractmethod
from typing import Any

import fake_useragent

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

from bots.constants import manifest_json, background_js
from bots.bot_configurations import  bot_config_parser_on, load_conf

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
    CONFIG_PARSE = bot_config_parser_on()
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

    def __start_or_reload_proxy(self, options):
        proxy = Proxie(
            self.USERNAME, self.PASSWORD,
            self.HOST, self.PORT
        )
        proxy.make_proxy()
        options.add_argument('--load-extension={}'.format(proxy.give_the_path()))
    
    def create_driver(self, use_proxy: bool = False) -> uc.Chrome:
        """
        Method for open your chrome browser
        """
        d = DesiredCapabilities.CHROME
        d['goog:loggingPrefs'] = { 'browser': 'ALL', 'driver': 'ALL' }

        options = uc.ChromeOptions()
        options.binary_location = '/opt/chrome/google-chrome'
        if use_proxy:
            self.__start_or_reload_proxy(options)
            
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--log-level=3")
        options.add_argument("--window-size=2560x1440")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--single-process")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument("--disable-application-cache")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.set_capability('useAutomationExtension', False)
        options.set_capability("excludeSwitches", ["enable-automation"])
        options.add_argument("--no-zygote")
        
        options.add_argument(f"--user-data-dir=/tmp/user-data-dir")
        options.add_argument(f"--data-path=/tmp/data-path")
        options.add_argument(f"--disk-cache-dir=/tmp/disk-cache-dir/")
        options.add_argument("--remote-debugging-port=9230")
        options.add_argument(f"user-agent={fake_useragent.UserAgent().random}")

        driver_path = ChromeDriverManager(path='/tmp').install()
        driver = uc.Chrome(
            headless=False,
            driver_executable_path=driver_path,
            desired_capabilities=d,
            service=Service(driver_path),
            options=options)
    
        driver.maximize_window()
        driver.implicitly_wait(20)

        return driver