import time
from procaaso_client.core.base import BaseApplication


class SyncApplication(BaseApplication):
    def start(self):
        self.running = True
        self.run()

    def stop(self):
        self.running = False
        if hasattr(self.client, "http_client") and hasattr(
            self.client.http_client, "close"
        ):
            self.client.http_client.close()  # Close the HTTP client properly

    def run(self):
        if self.startup_task is not None:
            self.startup_task()

        self.tasks.sort(key=lambda x: x[1])

        while self.running:
            for task, _, kwargs in self.tasks:
                task(**kwargs)
            time.sleep(self.execution_delay)

        if self.shutdown_task is not None:
            self.shutdown_task()

        # Ensure we close the HTTP client on shutdown
        self.stop()
