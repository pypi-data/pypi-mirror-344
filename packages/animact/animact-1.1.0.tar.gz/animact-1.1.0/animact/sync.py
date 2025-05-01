import httpx
from typing import List
from .base import BaseAnimact

class Animact(BaseAnimact):
    """Synchronous implementation of Animact."""
    
    def _get_json_url(self, url: str, key_chain: List[str]) -> str:
        """Synchronously get JSON URL from the API."""
        try:
            response = httpx.get(url)
            response.raise_for_status()
            data = response.json()
            for key in key_chain:
                data = data[key]
            return data
        except (httpx.HTTPError, KeyError, IndexError) as e:
            raise RuntimeError(f"API request failed: {e}")

# Create a default instance for direct import
default_instance = Animact()

# Make all methods available at module level
def __getattr__(name: str):
    return getattr(default_instance, name) 