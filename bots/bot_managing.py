import os
from abc import ABC, abstractmethod
from typing import Any
from random import choice

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
    def get_random_proxy():
        """ Returns a random proxy """
        return choice(Proxies.proxy_list)


class AbstractBot(ABC):

    @abstractmethod
    def work(self) -> Any: 
        pass

    @abstractmethod
    def generate_report(self) -> Any: 
        pass