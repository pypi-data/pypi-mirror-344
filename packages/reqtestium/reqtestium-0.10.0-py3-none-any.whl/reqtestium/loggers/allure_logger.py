import json

import allure
import curlify
from allure_commons.types import AttachmentType
from requests import Response

from .logger import LoggerProtocol


class AllureLogger(LoggerProtocol):
    @staticmethod
    def __attach_request_details(response: Response):
        if response.request.headers:
            allure.attach(
                body=str(response.request.headers),
                name="Заголовки запроса",
                attachment_type=AttachmentType.TEXT,
            )

        if response.request.body:
            try:
                json_content = json.dumps(
                    json.loads(response.request.body), indent=4, ensure_ascii=False
                )
                allure.attach(
                    body=json_content,
                    name="Тело запроса",
                    attachment_type=AttachmentType.JSON,
                    extension="json",
                )
            except (json.JSONDecodeError, TypeError):
                allure.attach(
                    body=response.request.body,
                    name="Тело запроса",
                    attachment_type=AttachmentType.TEXT,
                )

    @staticmethod
    def __attach_response_details(response: Response):
        allure.attach(
            body=str(response.status_code),
            name="Код ответа",
            attachment_type=AttachmentType.TEXT,
        )

        if response.text:
            try:
                json_response = response.json()
                allure.attach(
                    body=json.dumps(json_response, indent=4, ensure_ascii=False),
                    name="Тело ответа",
                    attachment_type=AttachmentType.JSON,
                    extension="json",
                )
            except ValueError:
                allure.attach(
                    body=response.text,
                    name="Тело ответа",
                    attachment_type=AttachmentType.TEXT,
                )

    @staticmethod
    def __attach_curl_command(response: Response):
        if response.request.body:
            curl_command = curlify.to_curl(response.request)
            allure.attach(
                body=curl_command,
                name="Curl запроса",
                attachment_type=AttachmentType.TEXT,
            )

    def log_request(self, response: Response):
        with allure.step(
            f"Отправляем {response.request.method} запрос на ручку: {str(response.request.url)}"
        ):
            self.__attach_request_details(response)
            self.__attach_response_details(response)
            self.__attach_curl_command(response)


allure_logger = AllureLogger()
