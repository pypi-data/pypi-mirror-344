⚠️ Disclaimer:
This library is intended for educational and authorized use only. 
The developer is NOT responsible for any misuse or violation of Discord's Terms of Service (ToS). 
Using selfbots on Discord is against their ToS and may result in account termination. 
Use at your own risk.

import json
from typing import Optional, Dict, List
from .models import Activity
from .client import Client

class Presence:
    """Handles Discord Rich Presence."""
    def __init__(self, client: Client):
        self.client = client

    async def set_presence(
        self,
        status: str = "online",
        activity: Optional[Activity] = None,
        afk: bool = False
    ) -> None:
        """Set the user's presence."""
        payload = {
            "op": 3,
            "d": {
                "status": status,
                "afk": afk,
                "activities": [activity.to_dict()] if activity else [],
                "since": 0,
            },
        }
        try:
            await self.client.ws.send(json.dumps(payload))
        except Exception as e:
            self.client.logger.error("Failed to set presence: %s", e)
            raise

    async def set_rich_presence(
        self,
        name: str,
        type: int = 0,
        url: Optional[str] = None,
        details: Optional[str] = None,
        state: Optional[str] = None,
        start_timestamp: Optional[int] = None,
        end_timestamp: Optional[int] = None,
        large_image: Optional[str] = None,
        large_text: Optional[str] = None,
        small_image: Optional[str] = None,
        small_text: Optional[str] = None,
        buttons: Optional[List[Dict[str, str]]] = None,
    ) -> None:
        """Set a rich presence activity."""
        timestamps = {}
        if start_timestamp:
            timestamps["start"] = start_timestamp
        if end_timestamp:
            timestamps["end"] = end_timestamp

        assets = {}
        if large_image:
            assets["large_image"] = large_image
        if large_text:
            assets["large_text"] = large_text
        if small_image:
            assets["small_image"] = small_image
        if small_text:
            assets["small_text"] = small_text

        activity = Activity(
            name=name,
            type=type,
            url=url,
            details=details,
            state=state,
            timestamps=timestamps if timestamps else None,
            assets=assets if assets else None,
            buttons=buttons,
        )
        await self.set_presence(activity=activity)