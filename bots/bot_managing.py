from abc import ABC, abstractmethod
from typing import Any

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from selenium_stealth import stealth

from bots.proxy_details import manifest_json, background_js
from config.settings import BASE_DIR

class Proxie:

    @property
    def give_the_path(self) -> str:
        return str(BASE_DIR) + '/bots/proxy/'

    @staticmethod
    def make_proxy() -> None:
        path = Proxie().give_the_path
        
        with open(path + 'background.js', 'w') as f:
            f.write(background_js)

        with open(path + 'manifest.json', 'w') as f:
            f.write(manifest_json)


class Bot(ABC):

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

    @staticmethod
    def create_driver(use_proxy: bool = False) -> uc.Chrome:
        """
        Method for open your chrome browser
        """
        options = uc.ChromeOptions()
        if use_proxy:
            proxy = Proxie()
            proxy.make_proxy()
            options.add_argument('--load-extension={}'.format(proxy.give_the_path))

        options.add_argument("--disable-web-security")
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument("--disable-application-cache")

        driver = uc.Chrome(
                            service=Service(ChromeDriverManager().install()), 
                            options=options
                            )

        # Make your driver more secretive
        stealth(driver,
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