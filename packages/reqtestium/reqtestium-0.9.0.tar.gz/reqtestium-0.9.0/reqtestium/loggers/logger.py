from abc import ABC, abstractmethod

from requests import Response


class LoggerProtocol(ABC):
    @abstractmethod
    def log_request(self, response: Response):
        pass
