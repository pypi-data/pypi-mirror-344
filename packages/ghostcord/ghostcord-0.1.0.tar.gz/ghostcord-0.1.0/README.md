⚠️ Disclaimer:
This library is intended for educational and authorized use only. 
The developer is NOT responsible for any misuse or violation of Discord's Terms of Service (ToS). 
Using selfbots on Discord is against their ToS and may result in account termination. 
Use at your own risk.

# GhostCord

GhostCord is a lightweight, async Python library for controlling Discord user accounts (selfbot behavior). It is designed to be modular, secure, and extensible, with zero external dependencies except `httpx` and `websockets`.

## Features
- Fully async with Python 3.8+ compatibility
- Send, edit, delete messages, and add reactions
- Read incoming DMs
- Rich Presence support (custom activities, images, timers, buttons)
- Smart rate limit handling
- Secure token handling (never logged or printed)
- Event system (`on_ready`, `on_message`, etc.)
- Prefixed command handler (e.g., `.ping`, `.say`)
- Automatic WebSocket reconnection
- Clean logging system (info/debug/error levels)

## Installation

1. Install the required dependencies:
   ```bash
   pip install httpx websockets
   ```

2. Clone or download the GhostCord repository:
   ```bash
   git clone https://github.com/xAI/GhostCord.git
   cd GhostCord
   ```

3. Install the library:
   ```bash
   pip install .
   ```

## Usage

### Basic Example
Create a file `bot.py`:

```python
import asyncio
from ghostcord import Client

client = Client(token="YOUR_TOKEN_HERE", prefix=".", log_level=20)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.command()
async def ping(message, args):
    await client.send_message(message.channel_id, "Pong!")

async def main():
    try:
        await client.connect()
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run the bot:
```bash
python bot.py
```

### Rich Presence Example
Set a custom Rich Presence:

```python
import asyncio
from ghostcord import Client
import time

client = Client(token="YOUR_TOKEN_HERE", prefix=".", log_level=20)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.presence.set_rich_presence(
        name="GhostCord",
        type=0,
        details="Running a selfbot",
        state="Developed by xAI",
        start_timestamp=int(time.time()),
        large_image="ghostcord_icon",
        large_text="GhostCord Library",
        buttons=[{"label": "Visit xAI", "url": "https://x.ai"}],
    )

async def main():
    try:
        await client.connect()
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Project Structure
```
GhostCord/
├── ghostcord/
│   ├── __init__.py
│   ├── client.py
│   ├── models.py
│   ├── utils.py
│   ├── errors.py
│   ├── presence.py
│   ├── events.py
│   ├── commands.py
│   └── ratelimit.py
├── examples/
│   ├── basic_bot.py
│   └── rich_presence.py
├── LICENSE
├── README.md
└── pyproject.toml
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue on GitHub.

## License
GhostCord is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.