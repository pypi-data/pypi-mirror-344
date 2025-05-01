from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class BaseAnimact(ABC):
    """Base class for Animact functionality."""
    
    NEKOS_BEST_BASE = 'https://nekos.best/api/v2'
    WAIFU_PICS_BASE = 'https://api.waifu.pics/sfw'
    NEKOS_LIFE_BASE = 'https://nekos.life/api/v2/img'
    
    def __init__(self):
        self._endpoints = {
            # Nekos.best endpoints
            'lurk': (self.NEKOS_BEST_BASE + '/lurk', ['results', 0, 'url']),
            'shoot': (self.NEKOS_BEST_BASE + '/shoot', ['results', 0, 'url']),
            'sleep': (self.NEKOS_BEST_BASE + '/sleep', ['results', 0, 'url']),
            'shrug': (self.NEKOS_BEST_BASE + '/shrug', ['results', 0, 'url']),
            'stare': (self.NEKOS_BEST_BASE + '/stare', ['results', 0, 'url']),
            'wave': (self.NEKOS_BEST_BASE + '/wave', ['results', 0, 'url']),
            'poke': (self.NEKOS_BEST_BASE + '/poke', ['results', 0, 'url']),
            'smile': (self.NEKOS_BEST_BASE + '/smile', ['results', 0, 'url']),
            'peck': (self.NEKOS_BEST_BASE + '/peck', ['results', 0, 'url']),
            'wink': (self.NEKOS_BEST_BASE + '/wink', ['results', 0, 'url']),
            'blush': (self.NEKOS_BEST_BASE + '/blush', ['results', 0, 'url']),
            'smug': (self.NEKOS_BEST_BASE + '/smug', ['results', 0, 'url']),
            'tickle': (self.NEKOS_BEST_BASE + '/tickle', ['results', 0, 'url']),
            'yeet': (self.NEKOS_BEST_BASE + '/yeet', ['results', 0, 'url']),
            'think': (self.NEKOS_BEST_BASE + '/think', ['results', 0, 'url']),
            'highfive': (self.NEKOS_BEST_BASE + '/highfive', ['results', 0, 'url']),
            'feed': (self.NEKOS_BEST_BASE + '/feed', ['results', 0, 'url']),
            'bite': (self.NEKOS_BEST_BASE + '/bite', ['results', 0, 'url']),
            'bored': (self.NEKOS_BEST_BASE + '/bored', ['results', 0, 'url']),
            'nom': (self.NEKOS_BEST_BASE + '/nom', ['results', 0, 'url']),
            'yawn': (self.NEKOS_BEST_BASE + '/yawn', ['results', 0, 'url']),
            'facepalm': (self.NEKOS_BEST_BASE + '/facepalm', ['results', 0, 'url']),
            'cuddle': (self.NEKOS_BEST_BASE + '/cuddle', ['results', 0, 'url']),
            'kick': (self.NEKOS_BEST_BASE + '/kick', ['results', 0, 'url']),
            'happy': (self.NEKOS_BEST_BASE + '/happy', ['results', 0, 'url']),
            'hug': (self.NEKOS_BEST_BASE + '/hug', ['results', 0, 'url']),
            'baka': (self.NEKOS_BEST_BASE + '/baka', ['results', 0, 'url']),
            'pat': (self.NEKOS_BEST_BASE + '/pat', ['results', 0, 'url']),
            'angry': (self.NEKOS_BEST_BASE + '/angry', ['results', 0, 'url']),
            'run': (self.NEKOS_BEST_BASE + '/run', ['results', 0, 'url']),
            'nod': (self.NEKOS_BEST_BASE + '/nod', ['results', 0, 'url']),
            'nope': (self.NEKOS_BEST_BASE + '/nope', ['results', 0, 'url']),
            'kiss': (self.NEKOS_BEST_BASE + '/kiss', ['results', 0, 'url']),
            'dance': (self.NEKOS_BEST_BASE + '/dance', ['results', 0, 'url']),
            'punch': (self.NEKOS_BEST_BASE + '/punch', ['results', 0, 'url']),
            'handshake': (self.NEKOS_BEST_BASE + '/handshake', ['results', 0, 'url']),
            'slap': (self.NEKOS_BEST_BASE + '/slap', ['results', 0, 'url']),
            'cry': (self.NEKOS_BEST_BASE + '/cry', ['results', 0, 'url']),
            'pout': (self.NEKOS_BEST_BASE + '/pout', ['results', 0, 'url']),
            'handhold': (self.NEKOS_BEST_BASE + '/handhold', ['results', 0, 'url']),
            'thumbsup': (self.NEKOS_BEST_BASE + '/thumbsup', ['results', 0, 'url']),
            'laugh': (self.NEKOS_BEST_BASE + '/laugh', ['results', 0, 'url']),
            
            # Waifu.pics endpoints
            'bully': (self.WAIFU_PICS_BASE + '/bully', ['url']),
            'lick': (self.WAIFU_PICS_BASE + '/lick', ['url']),
            'bonk': (self.WAIFU_PICS_BASE + '/bonk', ['url']),
            'glomp': (self.WAIFU_PICS_BASE + '/glomp', ['url']),
            'kill': (self.WAIFU_PICS_BASE + '/kill', ['url']),
            'cringe': (self.WAIFU_PICS_BASE + '/cringe', ['url']),
            
            # Nekos.life endpoints
            'spank': (self.NEKOS_LIFE_BASE + '/spank', ['url']),
        }

    @abstractmethod
    def _get_json_url(self, url: str, key_chain: List[str]) -> str:
        """Abstract method to get JSON URL that must be implemented by sync/async classes."""
        pass

    def __getattr__(self, name: str) -> Any:
        """Dynamic method creation for all endpoints."""
        if name in self._endpoints:
            url, key_chain = self._endpoints[name]
            
            def wrapper():
                return self._get_json_url(url, key_chain)
                
            return wrapper
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'") 