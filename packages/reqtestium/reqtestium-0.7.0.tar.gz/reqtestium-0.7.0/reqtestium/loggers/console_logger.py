import json
import logging

from requests import Response

from .logger import LoggerProtocol


class ConsoleLogger(LoggerProtocol):
    def __init__(self):
        self.logger = logging.getLogger("console_request_logger")
        self.logger.setLevel(logging.INFO)

        # Настройка вывода в консоль
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)

        # Очистка предыдущих обработчиков и добавление нового
        self.logger.handlers.clear()
        self.logger.addHandler(handler)

    def _format_request_details(self, response: Response) -> str:
        details = []
        details.append(f"\n{'=' * 50} REQUEST {'=' * 50}")
        details.append(f"URL: {response.request.method} {response.request.url}")

        if response.request.headers:
            details.append("\nHEADERS:")
            details.append(json.dumps(dict(response.request.headers), indent=4))

        if response.request.body:
            try:
                body = json.loads(response.request.body)
                details.append("\nBODY:")
                details.append(json.dumps(body, indent=4, ensure_ascii=False))
            except (json.JSONDecodeError, TypeError):
                details.append("\nBODY (raw):")
                details.append(str(response.request.body))

        return "\n".join(details)

    def _format_response_details(self, response: Response) -> str:
        details = []
        details.append(f"\n{'=' * 50} RESPONSE {'=' * 49}")
        details.append(f"STATUS CODE: {response.status_code}")

        if response.text:
            try:
                json_response = response.json()
                details.append("\nBODY:")
                details.append(json.dumps(json_response, indent=4, ensure_ascii=False))
            except ValueError:
                details.append("\nBODY (raw):")
                details.append(response.text)

        return "\n".join(details)

    def log_request(self, response: Response):
        try:
            request_details = self._format_request_details(response)
            response_details = self._format_response_details(response)

            self.logger.info(request_details)
            self.logger.info(response_details)
            self.logger.info("\n" + "=" * 108 + "\n")
        except Exception as e:
            self.logger.error(f"Error logging request: {str(e)}")


console_logger = ConsoleLogger()
