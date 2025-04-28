from reqtestium.loggers.logger import LoggerProtocol


class Configuration:
    def __init__(
        self,
        base_url: str,
        loggers: list[LoggerProtocol],
        headers: dict = None,
    ):
        self.base_url: str = base_url
        self.headers: dict = headers
        self.loggers: list[LoggerProtocol] = loggers or []
