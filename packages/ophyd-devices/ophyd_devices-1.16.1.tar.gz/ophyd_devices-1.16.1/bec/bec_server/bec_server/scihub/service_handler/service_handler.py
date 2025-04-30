from __future__ import annotations

import subprocess
import sys
from typing import TYPE_CHECKING

from bec_lib import messages
from bec_lib.endpoints import MessageEndpoints
from bec_lib.logger import bec_logger

if TYPE_CHECKING:
    from bec_lib.redis_connector import RedisConnector

logger = bec_logger.logger


class ServiceHandler:
    def __init__(self, connector: RedisConnector) -> None:
        self.connector = connector
        self.command = f"{sys.executable} -m bec_server.bec_server_utils.launch"

    def start(self):
        self.connector.register(
            MessageEndpoints.service_request(), cb=self.handle_service_request, parent=self
        )

    @staticmethod
    def handle_service_request(
        message: messages.ServiceRequestMessage, parent: ServiceHandler
    ) -> None:
        message = message.value
        if message.action == "restart":
            parent.on_restart()

    def on_restart(self):
        logger.info("Restarting services through service handler")
        subprocess.run(f"{self.command} restart", shell=True, check=True, start_new_session=True)
