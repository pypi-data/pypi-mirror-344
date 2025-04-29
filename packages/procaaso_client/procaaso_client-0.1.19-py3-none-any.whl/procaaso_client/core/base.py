from abc import ABC, abstractmethod
from typing import Optional, Type, Callable
from procaaso_log import get_logger
from pydantic import BaseModel

logger = get_logger(__name__)


class BaseHttpClient(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def post(self, url: str, json: dict = None, params: dict = None):
        pass

    @abstractmethod
    def get(self, url: str, params: dict = None):
        pass

    def _check_response(self, response):
        if response.status_code != 200:
            logger.error("Error:", response.text)
            response.raise_for_status()


class BaseHarnessClient(ABC):
    def __init__(self, http_client: BaseHttpClient):
        self.http_client = http_client

    @abstractmethod
    def post_startup_event(self) -> None:
        pass

    @abstractmethod
    def get_runtime_event(self) -> str:
        pass

    @abstractmethod
    def post_attribute_state(
        self,
        value: BaseModel,
        attribute_name: str,
        system_name: Optional [str] = None,
        component_name: Optional [str] = None,
        connector_name: Optional [str] = None,
        instrument_name: Optional [str] = None,
    ) -> None:
        pass

    @abstractmethod
    def get_attribute_state(
        self,
        attribute_name: str,
        system_name: Optional [str] = None,
        component_name: Optional [str] = None,
        connector_name: Optional [str] = None,
        instrument_name: Optional [str] = None,
        value_model: Type[BaseModel] = BaseModel(),
    ) -> BaseModel:
        pass

    @abstractmethod
    def get_system_io_maps_definition(self, system_name: Optional [str] = None) -> list:
        pass

    @abstractmethod
    def get_io_maps(
        self,
        system_name: Optional [str] = None,
        component_name: str = "",
        instrument_name: str = "",
        attribute_name: str = "",
        maps_query: str = "",
    ) -> list:
        pass


class BaseApplication(ABC):
    def __init__(self, client: BaseHarnessClient):
        self.tasks = []
        self.startup_task = None
        self.shutdown_task = None
        self.running = False
        self.client = client  # Assign the client parameter to self.client
        self.execution_delay = 0.005

    def expression(self, order: int, **kwargs):
        def decorator(task: Callable):
            self.add_task(task, order, kwargs)
            return task

        return decorator

    def add_task(self, task: Callable, order: int, kwargs):
        self.tasks.append((task, order, kwargs))

    def startup_expression(self, task: Callable):
        self.startup_task = task
        return task

    def shutdown_expression(self, task: Callable):
        self.shutdown_task = task
        return task

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def run(self):
        pass
