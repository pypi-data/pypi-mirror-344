import os
from typing import Optional
from maleo_foundation.clients.general.http import HTTPClientManager

class MaleoSecurityHTTPClientManager(HTTPClientManager):
    base_url:Optional[str] = None

    @classmethod
    def initialize(cls, base_url:Optional[str] = None) -> None:
        """Initialize the maleo-security client if not already initialized."""
        super().initialize()  #* Initialize HTTP Client Manager

        cls.base_url = base_url or os.getenv("MALEO_SECURITY_BASE_URL")
        if cls.base_url is None:
            raise ValueError("MALEO_SECURITY_BASE_URL environment variable must be set if no base_url is provided")
        cls.base_url += "/api"