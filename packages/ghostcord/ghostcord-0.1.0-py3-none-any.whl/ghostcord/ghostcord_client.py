⚠️ Disclaimer:
This library is intended for educational and authorized use only. 
The developer is NOT responsible for any misuse or violation of Discord's Terms of Service (ToS). 
Using selfbots on Discord is against their ToS and may result in account termination. 
Use at your own risk.

import asyncio
import logging
import httpx
import websockets
import json
import time
from typing import Optional, Dict, Callable, Any
from .models import User, Message
from .errors import AuthenticationError, RateLimitError, GhostCordError
from .events import EventHandler
from .commands import CommandHandler
from .ratelimit import RateLimiter
from .presence import Presence
from .utils import generate_nonce

logger = logging.getLogger("ghostcord")

class Client:
    """Main client for interacting with Discord as a selfbot."""
    def __init__(self, token: str, prefix: str = ".", log_level: int = logging.INFO):
        self.token = token  # Stored securely, never logged
        self.prefix = prefix
        self.http = httpx.AsyncClient(
            base_url="https://discord.com/api/v10",
            headers={"Authorization": f"Bot {self.token}", "User-Agent": "GhostCord/0.1.0"},
        )
        self.ws = None
        self.user: Optional[User] = None
        self.event_handler = EventHandler(self)
        self.command_handler = CommandHandler(self, prefix)
        self.ratelimiter = RateLimiter()
        self.presence = Presence(self)
        self._heartbeat_interval = None
        self._sequence = None
        self._session_id = None
        self._reconnect = True

        # Setup logging
        logging.basicConfig(level=log_level)
        logger.setLevel(log_level)

    async def connect(self) -> None:
        """Connect to Discord's Gateway."""
        try:
            gateway = await self.http.get("/gateway/bot")
            gateway_data = gateway.json()
            ws_url = gateway_data["url"]
            logger.info("Connecting to Gateway: %s", ws_url)

            async with websockets.connect(ws_url) as ws:
                self.ws = ws
                await self._handle_gateway()
        except Exception as e:
            logger.error("Connection failed: %s", e)
            if self._reconnect:
                logger.info("Attempting to reconnect in 5 seconds...")
                await asyncio.sleep(5)
                await self.connect()

    async def _handle_gateway(self) -> None:
        """Handle WebSocket events."""
        while self._reconnect:
            try:
                message = await self.ws.recv()
                data = json.loads(message)
                op = data.get("op")
                d = data.get("d")
                t = data.get("t")
                self._sequence = data.get("s")

                if op == 10:  # Hello
                    self._heartbeat_interval = d["heartbeat_interval"] / 1000
                    await self._start_heartbeat()
                    await self._identify()

                elif op == 11:  # Heartbeat ACK
                    logger.debug("Heartbeat acknowledged")

                elif t == "READY":
                    self.user = User(d["user"])
                    self._session_id = d["session_id"]
                    logger.info("Logged in as %s", self.user.username)
                    await self.event_handler.dispatch("on_ready")

                elif t == "MESSAGE_CREATE":
                    message = Message(d)
                    await self.event_handler.dispatch("on_message", message)
                    await self.command_handler.process_commands(message)

                elif t == "PRESENCE_UPDATE":
                    await self.event_handler.dispatch("on_presence_update", d)

            except websockets.exceptions.ConnectionClosed:
                logger.warning("WebSocket closed, attempting to reconnect...")
                break
            except Exception as e:
                logger.error("Error in WebSocket handler: %s", e)
                await self.event_handler.dispatch("on_error", e)

    async def _identify(self) -> None:
        """Send IDENTIFY payload to Discord."""
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "intents": 513,  # GUILDS and DIRECT_MESSAGES
                "properties": {
                    "os": "linux",
                    "browser": "GhostCord",
                    "device": "GhostCord",
                },
            },
        }
        await self.ws.send(json.dumps(payload))
        logger.debug("Sent IDENTIFY payload")

    async def _start_heartbeat(self) -> None:
        """Start sending heartbeats to keep the connection alive."""
        while True:
            await asyncio.sleep(self._heartbeat_interval)
            payload = {"op": 1, "d": self._sequence}
            try:
                await self.ws.send(json.dumps(payload))
                logger.debug("Sent heartbeat")
            except Exception as e:
                logger.error("Heartbeat failed: %s", e)
                break

    async def send_message(self, channel_id: str, content: str) -> Message:
        """Send a message to a channel."""
        async with self.ratelimiter:
            try:
                response = await self.http.post(
                    f"/channels/{channel_id}/messages",
                    json={"content": content, "nonce": generate_nonce()},
                )
                response.raise_for_status()
                return Message(response.json())
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    retry_after = e.response.json().get("retry_after", 5)
                    logger.warning("Rate limited, retrying after %s seconds", retry_after)
                    await asyncio.sleep(retry_after)
                    raise RateLimitError("Rate limit exceeded")
                raise GhostCordError(f"Failed to send message: {e}")

    async def edit_message(self, channel_id: str, message_id: str, content: str) -> Message:
        """Edit a message."""
        async with self.ratelimiter:
            try:
                response = await self.http.patch(
                    f"/channels/{channel_id}/messages/{message_id}",
                    json={"content": content},
                )
                response.raise_for_status()
                return Message(response.json())
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    retry_after = e.response.json().get("retry_after", 5)
                    logger.warning("Rate limited, retrying after %s seconds", retry_after)
                    await asyncio.sleep(retry_after)
                    raise RateLimitError("Rate limit exceeded")
                raise GhostCordError(f"Failed to edit message: {e}")

    async def delete_message(self, channel_id: str, message_id: str) -> None:
        """Delete a message."""
        async with self.ratelimiter:
            try:
                response = await self.http.delete(
                    f"/channels/{channel_id}/messages/{message_id}"
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    retry_after = e.response.json().get("retry_after", 5)
                    logger.warning("Rate limited, retrying after %s seconds", retry_after)
                    await asyncio.sleep(retry_after)
                    raise RateLimitError("Rate limit exceeded")
                raise GhostCordError(f"Failed to delete message: {e}")

    async def add_reaction(self, channel_id: str, message_id: str, emoji: str) -> None:
        """Add a reaction to a message."""
        async with self.ratelimiter:
            try:
                response = await self.http.put(
                    f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    retry_after = e.response.json().get("retry_after", 5)
                    logger.warning("Rate limited, retrying after %s seconds", retry_after)
                    await asyncio.sleep(retry_after)
                    raise RateLimitError("Rate limit exceeded")
                raise GhostCordError(f"Failed to add reaction: {e}")

    def event(self, func: Callable) -> Callable:
        """Decorator to register an event handler."""
        self.event_handler.register(func.__name__, func)
        return func

    def command(self, name: Optional[str] = None) -> Callable:
        """Decorator to register a command."""
        def decorator(func: Callable) -> Callable:
            self.command_handler.register(name or func.__name__, func)
            return func
        return decorator

    async def close(self) -> None:
        """Close the client connection."""
        self._reconnect = False
        if self.ws:
            await self.ws.close()
        await self.http.aclose()
        logger.info("Client closed")