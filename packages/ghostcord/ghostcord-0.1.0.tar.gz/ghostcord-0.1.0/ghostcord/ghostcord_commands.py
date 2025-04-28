⚠️ Disclaimer:
This library is intended for educational and authorized use only. 
The developer is NOT responsible for any misuse or violation of Discord's Terms of Service (ToS). 
Using selfbots on Discord is against their ToS and may result in account termination. 
Use at your own risk.

from typing import Callable, Dict, Any
from .client import Client
from .models import Message

class CommandHandler:
    """Handles prefixed commands."""
    def __init__(self, client: Client, prefix: str):
        self.client = client
        self.prefix = prefix
        self.commands: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable) -> None:
        """Register a command."""
        self.commands[name] = func
        self.client.logger.debug("Registered command: %s", name)

    async def process_commands(self, message: Message) -> None:
        """Process a message for commands."""
        if not message.content.startswith(self.prefix):
            return

        content = message.content[len(self.prefix):].strip()
        command_name, *args = content.split(" ", 1)
        args = args[0] if args else ""

        command = self.commands.get(command_name)
        if command:
            try:
                await command(message, args)
            except Exception as e:
                self.client.logger.error("Error in command %s: %s", command_name, e)