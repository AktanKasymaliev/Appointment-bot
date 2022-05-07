import os
from abc import ABC, abstractmethod, abstractstaticmethod
from typing import Any
from random import choice
import zipfile

from bots.proxy import plugin_file, manifest_json, background_js

import undetected_chromedriver as uc

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


class AbstractBot(ABC):

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

    def __open_browser(use_proxy: bool = False) -> uc.Chrome:
        """
        Method for open your chrome browser
        """
        pass