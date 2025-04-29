from procaaso_client.core.base import BaseHttpClient
import httpx


class SyncHttpClient(BaseHttpClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.client = httpx.Client(
            base_url=base_url,
            timeout=5.0,  # Set a reasonable timeout
            http2=True,  # Enable HTTP/2 for efficiency
            limits=httpx.Limits(max_keepalive_connections=100, max_connections=100),
        )

    def post(self, url: str, json: dict = None, params: dict = None):
        response = self.client.post(f"{self.base_url}{url}", json=json, params=params)
        if response.status_code != 200:
            raise Exception(
                f"Request failed with status code {response.status_code}: {response.text}"
            )
        return response

    def get(self, url: str, params: dict = None):
        response = self.client.get(f"{self.base_url}{url}", params=params)
        if response.status_code != 200:
            raise Exception(
                f"Request failed with status code {response.status_code}: {response.text}"
            )
        return response

    def close(self):
        """Close the client when shutting down."""
        self.client.close()


class AsyncHttpClient(BaseHttpClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=5.0,
            http2=True,
            limits=httpx.Limits(max_keepalive_connections=100, max_connections=100),
        )

    async def post(self, url: str, json: dict = None, params: dict = None):
        response = await self.client.post(
            f"{self.base_url}{url}", json=json, params=params
        )
        if response.status_code != 200:
            raise Exception(
                f"Request failed with status code {response.status_code}: {response.text}"
            )
        return response

    async def get(self, url: str, params: dict = None):
        response = await self.client.get(f"{self.base_url}{url}", params=params)
        if response.status_code != 200:
            raise Exception(
                f"Request failed with status code {response.status_code}: {response.text}"
            )
        return response

    async def close(self):
        """Close the async client when shutting down."""
        await self.client.aclose()
