⚠️ Disclaimer:
This library is intended for educational and authorized use only. 
The developer is NOT responsible for any misuse or violation of Discord's Terms of Service (ToS). 
Using selfbots on Discord is against their ToS and may result in account termination. 
Use at your own risk.

__version__ = "0.1.0"

from .client import Client
from .models import User, Message, Activity
from .errors import GhostCordError, RateLimitError, AuthenticationError
from .presence import Presence