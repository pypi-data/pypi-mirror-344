⚠️ Disclaimer:
This library is intended for educational and authorized use only. 
The developer is NOT responsible for any misuse or violation of Discord's Terms of Service (ToS). 
Using selfbots on Discord is against their ToS and may result in account termination. 
Use at your own risk.

from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    """Represents a Discord user."""
    id: str
    username: str
    discriminator: str
    avatar: Optional[str] = None

    def __init__(self, data: Dict[str, Any]):
        self.id = data["id"]
        self.username = data["username"]
        self.discriminator = data.get("discriminator", "0")
        self.avatar = data.get("avatar")

    def __str__(self) -> str:
        return f"{self.username}#{self.discriminator}"

@dataclass
class Message:
    """Represents a Discord message."""
    id: str
    channel_id: str
    content: str
    author: User
    timestamp: datetime

    def __init__(self, data: Dict[str, Any]):
        self.id = data["id"]
        self.channel_id = data["channel_id"]
        self.content = data["content"]
        self.author = User(data["author"])
        self.timestamp = datetime.fromisoformat(data["timestamp"])

@dataclass
class Activity:
    """Represents a Discord Rich Presence activity."""
    name: str
    type: int
    url: Optional[str] = None
    details: Optional[str] = None
    state: Optional[str] = None
    timestamps: Optional[Dict[str, int]] = None
    assets: Optional[Dict[str, str]] = None
    buttons: Optional[list[Dict[str, str]]] = None

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "name": self.name,
            "type": self.type,
        }
        if self.url:
            payload["url"] = self.url
        if self.details:
            payload["details"] = self.details
        if self.state:
            payload["state"] = self.state
        if self.timestamps:
            payload["timestamps"] = self.timestamps
        if self.assets:
            payload["assets"] = self.assets
        if self.buttons:
            payload["buttons"] = self.buttons
        return payload