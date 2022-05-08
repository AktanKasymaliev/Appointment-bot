import os
from abc import ABC, abstractmethod
from typing import Any
from random import choice
import zipfile

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

from bots.proxy import plugin_file, manifest_json, background_js


class Proxies:
    proxy_list = []

    @staticmethod
    def load_proxies(file_path: str):
        """
        Reads a text file with proxies
        :param file_path: Path to proxy file with proxies in <user>:<pas>@<ip>:<port> format each on one line
        """
        lst = []
        if file_path:
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    lst = [x for x in file.read().split('\n') if x.strip()]
            else:
                print('File: {}. Does not exist.'.format(file_path))
        Proxies.proxy_list = lst

    @staticmethod
    def get_random_proxy() -> str:
        """ Returns a random proxy """
        return choice(Proxies.proxy_list)

    @staticmethod
    def make_proxy() -> zipfile.ZipFile:
        random_proxy = Proxies.get_random_proxy()
        # 1 variant
        # auth, ip_port = random_proxy.split('@')
        # user, pwd = auth.split(':')
        # ip, port = ip_port.split(':')

        # # 2 variant
        user, pwd = "mix101JHHZLNC", "Aetoldv"
        ip, port = random_proxy.split(':') 

        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js % (ip, port, user, pwd))
        return plugin_file


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
            plugin_file = Proxies.make_proxy()
            options.add_extension(plugin_file)

        options.add_argument("--disable-web-security")
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument("--disable-application-cache")

        driver = uc.Chrome(
                            service=Service(ChromeDriverManager().install()), 
                            options=options
                            )
        driver.maximize_window()
        driver.implicitly_wait(10)

        return driver