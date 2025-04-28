from abc import ABC, abstractmethod
from urllib.parse import urljoin

import requests

from .api_response import APIResponse
from .configuration import Configuration


class HTTPClientProtocol(ABC):
    @abstractmethod
    def _make_request(self, handle: str, method: str, **kwargs) -> APIResponse:
        pass


class HTTPClient(HTTPClientProtocol):
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def _make_request(self, handle: str, method: str, **kwargs) -> APIResponse:
        full_url = urljoin(self.configuration.base_url, handle)

        headers = self.configuration.headers
        if headers:
            kwargs["headers"] = headers

        response = requests.request(method, url=full_url, **kwargs)

        if self.configuration.loggers:
            for logger in self.configuration.loggers:
                logger.log_request(response)

        return APIResponse(response)

    def post(self, handle: str, **kwargs) -> APIResponse:
        return self._make_request(handle=handle, method="POST", **kwargs)

    def get(self, handle: str, **kwargs) -> APIResponse:
        return self._make_request(handle=handle, method="GET", **kwargs)

    def put(self, handle: str, **kwargs) -> APIResponse:
        return self._make_request(handle=handle, method="PUT", **kwargs)

    def delete(self, handle: str, **kwargs) -> APIResponse:
        return self._make_request(handle=handle, method="DELETE", **kwargs)

    def patch(self, handle: str, **kwargs) -> APIResponse:
        return self._make_request(handle=handle, method="PATCH", **kwargs)
