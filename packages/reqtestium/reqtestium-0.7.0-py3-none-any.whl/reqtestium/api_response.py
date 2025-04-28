import allure
import requests
from allure import step
from jsonschema import ValidationError, validate

from .utils import get_diff


class ValueWrapper:
    def __init__(self, value):
        self._value = value

    def should_be_eq(self, expected_value):
        assert self._value == expected_value, (
            f"Разница в значениях:\n{get_diff(expected_value, self._value)}"
        )
        return self

    def should_be_greater_than(self, expected_value):
        assert self._value > expected_value, (
            f"Разница в значениях:\n{get_diff(expected_value, self._value)}"
        )
        return self

    def __repr__(self):
        return repr(self._value)

    def __str__(self):
        return str(self._value)

    def __int__(self):
        return int(self._value)

    def __len__(self):
        return len(self._value)

    def __getitem__(self, key):
        return self._value[key]

    def __eq__(self, other):
        return self._value == other

    def __ne__(self, other):
        return self._value != other

    def items(self):
        if isinstance(self._value, dict):
            return self._value.items()
        raise AttributeError("'ValueWrapper' object has no attribute 'items'")

    def keys(self):
        if isinstance(self._value, dict):
            return self._value.keys()
        raise AttributeError("'ValueWrapper' object has no attribute 'keys'")

    def values(self):
        if isinstance(self._value, dict):
            return self._value.values()
        raise AttributeError("'ValueWrapper' object has no attribute 'values'")


class StatusCode:
    """Класс для работы с кодом статуса ответа."""

    def __init__(self, status_code: int):
        self._status_code = status_code

    def __repr__(self):
        return repr(self._status_code)

    def __str__(self):
        return str(self._status_code)

    def should_be_eq(self, expected_value: int):
        """Проверяет, что текущий код статуса равен ожидаемому."""
        with step(f"Проверяем, что статус код равен {expected_value}"):
            assert self._status_code == expected_value, (
                f"Ожидался статус код: {expected_value}, но получен: {self._status_code}"
            )
        return self


class JsonResponse:
    def __init__(self, json: dict):
        self._json = json

    def __repr__(self):
        """Возвращает строковое представление JSON-ответа."""
        return repr(self._json)

    def __str__(self):
        """Возвращает строковое представление JSON-ответа."""
        return str(self._json)

    # TODO: подумать как улучшить эту часть.
    def should_be_eq(self, expected_value):
        """Проверяет, что JSON ответа равен ожидаемому значению."""
        return ValueWrapper(self._json).should_be_eq(expected_value)

    def value_with_key(self, key: str) -> ValueWrapper:
        return ValueWrapper(self._json[key])

    @property
    def length(self) -> ValueWrapper:
        return ValueWrapper(len(self._json))

    def without_fields(self, fields: list) -> ValueWrapper:
        return ValueWrapper({k: v for k, v in self._json.items() if k not in fields})

    def with_nested_value(self, keys: list) -> ValueWrapper:
        response_json = self._json
        for key in keys:
            if isinstance(response_json, dict) and key in response_json:
                response_json = response_json[key]
            elif isinstance(response_json, list) and isinstance(key, int):
                if 0 <= key < len(response_json):
                    response_json = response_json[key]
                else:
                    raise IndexError(f"Индекс {key} выходит за пределы списка")
            else:
                raise KeyError(f"Ключ или индекс '{key}' не найден")
        return ValueWrapper(response_json)

    def schema_should_be_eq(self, expected_schema: dict):
        response_json = self._json
        try:
            validate(instance=response_json, schema=expected_schema)
        except ValidationError as e:
            error_msg = f"Ошибка валидации схемы: {e}"
            allure.attach(
                str(e),
                name="Schema Validation Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            raise AssertionError(error_msg)
        return ValueWrapper(response_json)


class APIResponse:
    """Основной класс для работы с ответом API."""

    def __init__(self, response: requests.Response):
        self.__response = response
        self.status_code = StatusCode(response.status_code)

        if response.content:
            self.json = JsonResponse(response.json())

    @property
    def raw_response(self) -> requests.Response:
        """Возвращает оригинальный объект response из библиотеки requests."""
        return self.__response
