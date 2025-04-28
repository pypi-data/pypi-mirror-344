import os
from typing import Optional
from maleo_foundation.clients.general.http import HTTPClientManager

class MaleoMetadataHTTPClientManager(HTTPClientManager):
    base_url:Optional[str] = None

    @classmethod
    def initialize(cls, base_url:Optional[str] = None) -> None:
        """Initialize the maleo-metadata client if not already initialized."""
        super().initialize()  #* Initialize HTTP Client Manager

        cls.base_url = base_url or os.getenv("MALEO_METADATA_BASE_URL")
        if cls.base_url is None:
            raise ValueError("MALEO_METADATA_BASE_URL environment variable must be set if no base_url is provided")
        cls.base_url += "/api"