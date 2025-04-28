⚠️ Disclaimer:
This library is intended for educational and authorized use only. 
The developer is NOT responsible for any misuse or violation of Discord's Terms of Service (ToS). 
Using selfbots on Discord is against their ToS and may result in account termination. 
Use at your own risk.

class GhostCordError(Exception):
    """Base exception for GhostCord errors."""
    pass

class RateLimitError(GhostCordError):
    """Raised when rate limit is exceeded."""
    pass

class AuthenticationError(GhostCordError):
    """Raised when authentication fails."""
    pass