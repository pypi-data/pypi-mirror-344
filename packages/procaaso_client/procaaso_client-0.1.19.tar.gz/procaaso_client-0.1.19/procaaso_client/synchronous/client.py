from typing import Optional, Type
from procaaso_client.core.http_clients import SyncHttpClient
from procaaso_client.core.base import BaseHarnessClient
from procaaso_client.core.client_models import Attribute
from pydantic import BaseModel
from procaaso_log import get_logger

logger = get_logger(__name__)


class SyncHarnessClient(BaseHarnessClient):
    def __init__(self, http_client: SyncHttpClient, system_name: Optional[str] = ""):
        self.http_client = http_client
        self.count = 0
        self.system_name = system_name

    def get_runtime_event(self) -> str:
        response = self.http_client.get(
            "/runtimeEvent", params={"event": "defaultSystem"}
        )
        self.http_client._check_response(response)
        data = response.json()

        try:
            self.system_name = data["name"]
        except Exception as e:
            raise e
        return data["event"]

    def post_startup_event(self) -> None:
        response = self.http_client.post(
            "/runtimeEvent", params={"event": "clearCache"}
        )
        self.http_client._check_response(response)

    def post_attribute_state(
        self,
        value: BaseModel,
        attribute_name: str,
        system_name: Optional[str] = None,
        component_name: Optional[str] = None,
        connector_name: Optional[str] = None,
        instrument_name: Optional[str] = None,
    ) -> None:
        attribute = Attribute(value=value)
        json_data = attribute.to_json()
        response = self.http_client.post(
            "/attributeStates",
            json=json_data,
            params={
                "system": system_name or self.system_name,
                "component": component_name,
                "connector": connector_name,
                "instrument": instrument_name,
                "attribute": attribute_name,
            },
        )
        self.http_client._check_response(response)

    def get_attribute_state(
        self,
        attribute_name: str,
        system_name: Optional[str] = None,
        component_name: Optional[str] = None,
        connector_name: Optional[str] = None,
        instrument_name: Optional[str] = None,
        value_model: Type[BaseModel] = BaseModel(),
    ) -> BaseModel:
        response = self.http_client.get(
            "/attributeStates",
            params={
                "system": system_name or self.system_name,
                "component": component_name,
                "connector": connector_name,
                "instrument": instrument_name,
                "attribute": attribute_name,
            },
        )
        if response.status_code == 400:
            logger.error("Error:", response.text)
            response.raise_for_status()
        elif response.status_code == 404:
            logger.error("Error:", response.text)
            return value_model()
        elif response.status_code != 200:
            logger.error("Error:", response.text)
            response.raise_for_status()

        json_data = response.json()

        attribute = Attribute.from_json(json_data, value_model=value_model)
        return attribute.value

    def get_system_io_maps_definition(self, system_name: Optional[str] = None) -> list:
        response = self.http_client.get(
            "/ioMaps/system", params={"system": system_name or self.system_name}
        )
        self.http_client._check_response(response)
        return response.json()

    def get_io_maps(
        self,
        system_name: Optional[str] = None,
        component_name: str = "",
        instrument_name: str = "",
        attribute_name: str = "",
        maps_query: str = "",
    ) -> list:
        response = self.http_client.get(
            "/ioMaps",
            params={
                "system": system_name or self.system_name,
                "component": component_name,
                "attribute": attribute_name,
                "instrument": instrument_name,
                "maps_query": maps_query,
            },
        )
        self.http_client._check_response(response)
        return response.json()

    def close(self):
        """Ensure the HTTP client is properly closed."""
        if hasattr(self.http_client, "close"):
            self.http_client.close()
