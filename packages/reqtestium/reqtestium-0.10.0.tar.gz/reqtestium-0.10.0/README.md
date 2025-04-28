## Краткое описание функционала 

1. Базовая конфигурация для отправки всех api запросов 
2. Логгирование в терминал, allure отчет 
3. Удобное fluent сравнение ожидаемого результата с фактическим результатом
4. Валидация json схемы

## Пример использования 

```
# from reqtestium import allure_logger
from reqtestium import Configuration, HTTPClient, console_logger

config = Configuration(
    base_url="https://petstore.swagger.io",
    # Так же можно создавать свой logger на основе LoggerProtocol
    # from reqtestium.loggers.logger import LoggerProtocol
    loggers=[console_logger],
)
client = HTTPClient(config)


response = client.post(
    "/v2/user",
    json={
        "id": 0,
        "username": "string",
        "firstName": "string",
        "lastName": "string",
        "email": "string",
        "password": "string",
        "phone": "string",
        "userStatus": 0,
    },
)

# Можем проверять конкретные значения или весь ответ
# response.json.should_be_eq()
response.status_code.should_be_eq(200)
response.json.value_with_key("code").should_be_eq(200)
response.json.value_with_key("type").should_be_eq("unknown")

# Можем проверить приходящий json на соответствие схеме.
response.json.schema_should_be_eq(
    {
        "type": "object",
        "properties": {
            "code": {"type": "integer"},
            "type": {"type": "string"},
            "message": {"type": "string"},
        },
        "required": ["code", "type", "message"],
        "additionalProperties": False,
    }
)


# Можем проверить ответ исключив некоторые поля
response.json.without_fields(["type", "message"]).should_be_eq({"code": 200})


# Можем получить оригинальный Response из requests.
print(response.raw_response)


response.json.length.should_be_eq(3)
```