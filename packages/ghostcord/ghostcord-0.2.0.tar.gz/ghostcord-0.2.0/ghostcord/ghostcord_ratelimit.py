⚠️ Disclaimer:
This library is intended for educational and authorized use only. 
The developer is NOT responsible for any misuse or violation of Discord's Terms of Service (ToS). 
Using selfbots on Discord is against their ToS and may result in account termination. 
Use at your own risk.

import asyncio
from typing import Optional
from contextlib import asynccontextmanager

class RateLimiter:
    """Handles Discord API rate limits."""
    def __init__(self):
        self.lock = asyncio.Lock()
        self.requests = 0
        self.reset_time: Optional[float] = None

    @asynccontextmanager
    async def __aenter__(self):
        async with self.lock:
            if self.reset_time and self.reset_time > asyncio.get_event_loop().time():
                await asyncio.sleep(self.reset_time - asyncio.get_event_loop().time())
            self.requests += 1
            if self.requests >= 50:  # Discord global rate limit
                self.reset_time = asyncio.get_event_loop().time() + 1.0
                self.requests = 0
        yield

    async def __aexit__(self, exc_type, exc, tb):
        pass