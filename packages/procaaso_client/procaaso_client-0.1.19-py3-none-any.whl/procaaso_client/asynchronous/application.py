import asyncio
from procaaso_client.core.base import BaseApplication, BaseHarnessClient


class AsyncApplication(BaseApplication):
    def __init__(self, client: BaseHarnessClient):
        super().__init__(client=client)
        self.stop_event = asyncio.Event()

    async def start(self):
        self.running = True
        await self.run()

    async def stop(self):
        self.stop_event.set()
        if hasattr(self.client, "http_client") and hasattr(
            self.client.http_client, "close"
        ):
            await self.client.http_client.close()  # Ensure we close the HTTP client properly

    async def run(self):
        if self.startup_task is not None:
            await self.startup_task()

        self.tasks.sort(key=lambda x: x[1])

        while not self.stop_event.is_set():

            for task, _, kwargs in self.tasks:
                await task(**kwargs)
            await asyncio.sleep(self.execution_delay)

        if self.shutdown_task is not None:
            await self.shutdown_task()

        # Ensure we clean up resources
        await self.stop()
