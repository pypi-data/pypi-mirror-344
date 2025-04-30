import aiohttp
import hmac
import hashlib
import time
from typing import Dict, Any, Optional
from urllib.parse import urlencode

class APIClient:
    ASTER_BASE_URL = "https://fapi.asterdex.com"
    ASTER_TESTNET_BASE_URL = "https://testnet.asterdex.com"
    BINANCE_BASE_URL = "https://fapi.binance.com"
    BINANCE_TESTNET_BASE_URL = "https://testnet.binancefuture.com"
    
    def __init__(self, api_key: str, api_secret: str, provider: str = "aster", testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = ""
        if provider == "binance":
            self.base_url = self.BINANCE_TESTNET_BASE_URL if testnet else self.BINANCE_BASE_URL
        elif provider == "aster":
            self.base_url = self.ASTER_TESTNET_BASE_URL if testnet else self.ASTER_BASE_URL
        else:
            raise ValueError("Invalid provider")
        
    def _get_signature(self, params: Dict[str, Any]) -> str:
        """Generate HMAC SHA256 signature for private endpoints."""
        query_string = urlencode(params)
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None, 
        security_type: str = "NONE"
    ) -> Dict[str, Any]:
        """Make an HTTP request to the exchange API with security type handling."""
        if params is None:
            params = {}

        headers = {}
        url = f"{self.base_url}{endpoint}"
        request_params = None
        json_body = None

        if security_type in ("TRADE", "USER_DATA"):  # SIGNED endpoints
            params['timestamp'] = int(time.time() * 1000)
            params_for_sig = params.copy()
            query_string = urlencode(params_for_sig)
            signature = hmac.new(
                self.api_secret.encode('utf-8'),
                query_string.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            params['signature'] = signature
            headers['X-MBX-APIKEY'] = self.api_key
            if method == 'POST':
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                # For signed POST, send as urlencoded body
                request_params = f"{urlencode(params)}"
                json_body = None
            else:
                request_params = f"{urlencode(params)}"
                json_body = None
        elif security_type in ("USER_STREAM", "MARKET_DATA"):
            headers['X-MBX-APIKEY'] = self.api_key
            request_params = params if method == 'GET' else None
            json_body = params if method != 'GET' else None
        else:
            request_params = params if method == 'GET' else None
            json_body = params if method != 'GET' else None

        async with aiohttp.ClientSession() as session:
            if method == 'POST' and security_type in ("TRADE", "USER_DATA"):
                async with session.request(method, url, headers=headers, data=request_params) as response:
                    return await response.json()
            else:
                async with session.request(method, url, headers=headers, params=request_params, json=json_body) as response:
                    return await response.json()
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, security_type: str = "NONE") -> Dict[str, Any]:
        """Make a GET request to the exchange API with security type."""
        return await self._request('GET', endpoint, params, security_type)
    
    async def post(self, endpoint: str, params: Optional[Dict[str, Any]] = None, security_type: str = "TRADE") -> Dict[str, Any]:
        """Make a POST request to the exchange API with security type."""
        return await self._request('POST', endpoint, params, security_type)
    
    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None, security_type: str = "TRADE") -> Dict[str, Any]:
        """Make a DELETE request to the exchange API with security type."""
        return await self._request('DELETE', endpoint, params, security_type) 