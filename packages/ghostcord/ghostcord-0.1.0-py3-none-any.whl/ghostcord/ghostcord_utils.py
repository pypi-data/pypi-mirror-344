⚠️ Disclaimer:
This library is intended for educational and authorized use only. 
The developer is NOT responsible for any misuse or violation of Discord's Terms of Service (ToS). 
Using selfbots on Discord is against their ToS and may result in account termination. 
Use at your own risk.

import random
import time

def generate_nonce() -> str:
    """Generate a unique nonce for Discord API requests."""
    return str(int(time.time() * 1000)) + str(random.randint(1000, 9999))