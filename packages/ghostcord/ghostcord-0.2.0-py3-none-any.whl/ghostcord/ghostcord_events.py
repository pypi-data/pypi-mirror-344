⚠️ Disclaimer:
This library is intended for educational and authorized use only. 
The developer is NOT responsible for any misuse or violation of Discord's Terms of Service (ToS). 
Using selfbots on Discord is against their ToS and may result in account termination. 
Use at your own risk.

from typing import Callable, Dict, Any
from .client import Client

class EventHandler:
    """Handles event registration and dispatching."""
    def __init__(self, client: Client):
        self.client = client
        self.events: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable) -> None:
        """Register an event handler."""
        self.events[name] = func
        self.client.logger.debug("Registered event: %s", name)

    async def dispatch(self, event: str, *args, **kwargs) -> None:
        """Dispatch an event to its handler."""
        handler = self.events.get(event)
        if handler:
            try:
                await handler(*args, **kwargs)
            except Exception as e:
                self.client.logger.error("Error in event %s: %s", event, e)