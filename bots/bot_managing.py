import os
from abc import ABC, abstractmethod
from typing import Any
from configparser import ConfigParser
from pyvirtualdisplay import Display

import fake_useragent

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from selenium_stealth import stealth

from bots.constants import manifest_json, background_js
from bots.bot_configurations import  load_conf

PROXY = "PROXY"
PROXY_FILES_PATH = "PROXY_FILES_PATH"

class Proxie:
    def __init__(self, username: str, password: str, host: str, port: int) -> None:
        self.USERNAME = username
        self.PASSWORD = password
        self.HOST = host
        self.PORT = port
        
        config_parse = ConfigParser()
        config_parse.read("bot_settings.ini")

        self.PROXY_FILES_PATH = load_conf(config_parse, PROXY, PROXY_FILES_PATH)
        print(self.PROXY_FILES_PATH)


    def give_the_path(self) -> str:
        # On prod it should be /tmp
        proxy_files_path = self.PROXY_FILES_PATH + '/bots/proxy/'
        print('proxy_files_path', proxy_files_path)
        return proxy_files_path

    def make_proxy(self) -> None:
        path = self.give_the_path()
        # Create path
        os.makedirs(path, exist_ok=True)
        background_js_file = path + 'background.js'
        manifest_json_file = path + 'manifest.json'

        with open(background_js_file, 'w') as f:
            f.write(background_js % (
                self.HOST, self.PORT, 
                self.USERNAME, self.PASSWORD
                    )
                )

        with open(manifest_json_file, 'w') as f:
            f.write(manifest_json)


class Bot(ABC):
    CONFIG_PARSE = ConfigParser()
    CONFIG_PARSE.read("bot_settings.ini")

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
        
        browser_exec_path = '/opt/google/chrome/chrome'
        if 'LAMBDA_TASK_ROOT' in os.environ:
            display = Display(visible=False, extra_args=[':25'], size=(2560, 1440)) 
            display.start()
            print('Started Display')
            options.add_argument("window-size=2560x1440")
            options.add_argument("--user-data-dir=/tmp/chrome-user-data")
            options.add_argument("--remote-debugging-port=9222")
            options.binary_location = browser_exec_path
        else:
            options.add_argument("--headless")

        options.add_argument("--no-sandbox")
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
        options.add_argument(f"user-agent={fake_useragent.UserAgent().random}")
        
        driver_path = ChromeDriverManager(path='/tmp').install()

        driver = uc.Chrome(
            driver_executable_path=driver_path,
            browser_executable_path=browser_exec_path,
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