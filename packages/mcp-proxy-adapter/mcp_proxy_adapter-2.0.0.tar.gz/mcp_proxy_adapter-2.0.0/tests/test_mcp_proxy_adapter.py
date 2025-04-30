"""
Тесты для MCPProxyAdapter с акцентом на 100% покрытие кода,
включая обработку ошибок, пограничные случаи и неполное заполнение сигнатур.
"""
import json
import logging
import sys
import os
import pytest
import tempfile
from unittest.mock import MagicMock, patch

# Добавляем путь к исходникам
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.testclient import TestClient

# Импортируем напрямую из src
from src.adapter import MCPProxyAdapter, configure_logger
from src.models import JsonRpcRequest, JsonRpcResponse, MCPProxyConfig, MCPProxyTool

# Тестовые функции-команды
def success_command(value: int = 1) -> dict:
    """Тестовая команда, завершающаяся успешно."""
    return {"result": value * 2}

def error_command() -> None:
    """Тестовая команда, генерирующая ошибку."""
    raise ValueError("Тестовая ошибка")

def param_command(required_param: str, optional_param: int = 0) -> dict:
    """Тестовая команда с обязательным и необязательным параметрами."""
    return {"required": required_param, "optional": optional_param}

def complex_param_command(array_param: list, object_param: dict, bool_param: bool = True) -> dict:
    """Тестовая команда со сложными типами параметров."""
    return {
        "array_length": len(array_param),
        "object_keys": list(object_param.keys()),
        "bool_value": bool_param
    }

def type_error_command(param: int) -> dict:
    """Команда, которая вызовет TypeError при неправильном типе параметра."""
    return {"param": param + 1}  # Требуется int

# Мок для диспетчера команд
class MockDispatcher:
    """Mock for command dispatcher in tests."""
    
    def __init__(self):
        self.commands = {
            "success": success_command,
            "error": error_command,
            "param": param_command,
            "execute": self.execute_from_params
        }
        self.commands_info = {
            "success": {
                "description": "Successful command",
                "params": {
                    "value": {
                        "type": "integer",
                        "description": "Input value",
                        "required": False,
                        "default": 1
                    }
                }
            },
            "error": {
                "description": "Command with error",
                "params": {}
            },
            "param": {
                "description": "Command with parameters",
                "params": {
                    "required_param": {
                        "type": "string",
                        "description": "Required parameter",
                        "required": True
                    },
                    "optional_param": {
                        "type": "integer",
                        "description": "Optional parameter",
                        "required": False,
                        "default": 0
                    }
                }
            },
            "execute": {
                "description": "Universal command for executing other commands",
                "params": {
                    "query": {
                        "type": "string",
                        "description": "Command or query to execute",
                        "required": False
                    }
                }
            },
            "complex_param": {
                "description": "Command with complex parameters",
                "params": {
                    "array_param": {
                        "type": "array",
                        "description": "Array of values",
                        "required": True
                    },
                    "object_param": {
                        "type": "object",
                        "description": "Object",
                        "required": True
                    },
                    "bool_param": {
                        "type": "boolean",
                        "description": "Boolean value",
                        "required": False,
                        "default": True
                    }
                }
            },
            "type_error": {
                "description": "Command that will raise TypeError",
                "params": {
                    "param": {
                        "type": "integer",
                        "description": "Integer parameter",
                        "required": True
                    }
                }
            }
        }
    
    def execute_from_params(self, **params):
        """Executes command based on parameters."""
        if "query" in params and params["query"] in self.commands:
            command = params.pop("query")
            return self.execute(command, **params)
        return {
            "available_commands": self.get_valid_commands(),
            "received_params": params
        }
    
    def execute(self, command, **params):
        """Executes command with specified parameters."""
        if command not in self.commands:
            raise KeyError(f"Unknown command: {command}")
        return self.commands[command](**params)
    
    def get_valid_commands(self):
        """Returns list of available commands."""
        return list(self.commands.keys())
    
    def get_command_info(self, command):
        """Returns information about command."""
        return self.commands_info.get(command)
    
    def get_commands_info(self):
        """Returns information about all commands."""
        return self.commands_info

# Мок для CommandRegistry
class MockRegistry:
    """Мок для CommandRegistry в тестах."""
    
    def __init__(self, use_openapi_generator=False):
        self.dispatcher = MockDispatcher()
        self.generators = []
        self.use_openapi_generator = use_openapi_generator
    
    def get_commands_info(self):
        """Возвращает информацию о командах из диспетчера."""
        return self.dispatcher.get_commands_info()
    
    def add_generator(self, generator):
        """Добавляет генератор API."""
        self.generators.append(generator)
        if hasattr(generator, 'set_dispatcher'):
            generator.set_dispatcher(self.dispatcher)

# Мок для OpenApiGenerator
class MockOpenApiGenerator:
    """Мок для OpenApiGenerator в тестах."""
    
    def __init__(self, **kwargs):
        self.dispatcher = None
        self.kwargs = kwargs
    
    def set_dispatcher(self, dispatcher):
        """Устанавливает диспетчер команд."""
        self.dispatcher = dispatcher
    
    def generate_schema(self):
        """Генерирует схему OpenAPI."""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": self.kwargs.get("title", "API"),
                "version": self.kwargs.get("version", "1.0.0"),
                "description": self.kwargs.get("description", "API description")
            },
            "paths": {
                "/test": {
                    "get": {
                        "summary": "Test endpoint",
                        "responses": {
                            "200": {
                                "description": "Successful response"
                            }
                        }
                    }
                }
            }
        }

# Фикстуры для тестов
@pytest.fixture
def registry():
    """Возвращает мок реестра команд."""
    return MockRegistry()

@pytest.fixture
def registry_with_openapi():
    """Возвращает мок реестра команд с поддержкой OpenAPI."""
    registry = MockRegistry(use_openapi_generator=True)
    return registry

@pytest.fixture
def adapter(registry):
    """Возвращает настроенный адаптер для тестов."""
    return MCPProxyAdapter(registry)

@pytest.fixture
def adapter_with_openapi(registry):
    """Возвращает адаптер с поддержкой OpenAPI для тестов."""
    with patch('src.adapter.OpenApiGenerator', MockOpenApiGenerator):
        return MCPProxyAdapter(registry)

@pytest.fixture
def test_app(adapter):
    """Создает тестовое приложение FastAPI с настроенным адаптером."""
    app = FastAPI()
    adapter.register_endpoints(app)
    return TestClient(app)

@pytest.fixture
def custom_endpoint_adapter(registry):
    """Возвращает адаптер с кастомным эндпоинтом."""
    return MCPProxyAdapter(registry, cmd_endpoint="/api/execute")

@pytest.fixture
def custom_endpoint_app(custom_endpoint_adapter):
    """Создает тестовое приложение с адаптером, имеющим кастомный эндпоинт."""
    app = FastAPI()
    custom_endpoint_adapter.register_endpoints(app)
    return TestClient(app)

@pytest.fixture
def no_schema_adapter(registry):
    """Возвращает адаптер без включения схемы OpenAPI."""
    return MCPProxyAdapter(registry, include_schema=False)

@pytest.fixture
def no_schema_app(no_schema_adapter):
    """Создает тестовое приложение без эндпоинта схемы OpenAPI."""
    app = FastAPI()
    no_schema_adapter.register_endpoints(app)
    return TestClient(app)

@pytest.fixture
def no_optimize_adapter(registry):
    """Возвращает адаптер без оптимизации схемы."""
    return MCPProxyAdapter(registry, optimize_schema=False)

@pytest.fixture
def custom_prefix_adapter(registry):
    """Возвращает адаптер с пользовательским префиксом инструментов."""
    return MCPProxyAdapter(registry, tool_name_prefix="custom_")

@pytest.fixture
def custom_logger():
    """Создает настраиваемый логгер для тестов."""
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.DEBUG)
    
    # Очищаем обработчики, если они были добавлены в предыдущих тестах
    if logger.handlers:
        logger.handlers = []
    
    # Добавляем обработчик, который будет записывать сообщения в список
    log_records = []
    
    class ListHandler(logging.Handler):
        def emit(self, record):
            log_records.append(self.format(record))
    
    handler = ListHandler()
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger, log_records

# Тесты для основных сценариев
def test_successful_command_execution(test_app):
    """Тест успешного выполнения команды."""
    response = test_app.post("/cmd", json={
        "jsonrpc": "2.0",
        "method": "success",
        "params": {"value": 5},
        "id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == {"result": 10}

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 
