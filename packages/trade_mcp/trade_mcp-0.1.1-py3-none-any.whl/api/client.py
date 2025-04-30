from typing import Optional
from api.http_utils import APIClient

class APIClientManager:
    _instance: Optional[APIClient] = None
    
    @classmethod
    def initialize(cls, api_key: str, api_secret: str, provider: str = "aster", testnet: bool = True) -> None:
        """Initialize the API client with credentials for any supported exchange.
        
        Args:
            api_key: Exchange API key
            api_secret: Exchange API secret
            testnet: Whether to use testnet (default: True)
        """
        cls._instance = APIClient(
            api_key=api_key,
            api_secret=api_secret,
            provider=provider,
            testnet=testnet
        )
        
    @classmethod
    def get_client(cls) -> APIClient:
        """Get the initialized API client instance."""
        if cls._instance is None:
            raise RuntimeError("API client not initialized. Call initialize() first.")
        return cls._instance 