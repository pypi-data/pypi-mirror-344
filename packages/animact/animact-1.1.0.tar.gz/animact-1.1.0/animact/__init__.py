"""
Animact - Anime-themed action and reaction image API wrapper for Python.
"""

from .sync import Animact
from .async_api import AsyncAnimact

# Create default instances
_sync_instance = Animact()
async_animact = AsyncAnimact()

# Make sync instance available as 'animact'
animact = _sync_instance

# Make all methods available at module level for sync usage
def __getattr__(name: str):
    return getattr(_sync_instance, name)

__version__ = "1.1.0"
__all__ = [
    "Animact",  # Sync class
    "AsyncAnimact",  # Async class
    "animact",  # Default sync instance
    "async_animact",  # Default async instance
]