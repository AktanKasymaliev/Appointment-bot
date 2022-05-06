from abc import ABC, abstractmethod
from typing import Any

class AbstractBot(ABC):

    @abstractmethod
    def work(self) -> Any: 
        pass

    @abstractmethod
    def generate_report(self) -> Any: 
        pass