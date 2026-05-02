from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, default_limits=[])

PUBLIC_RATE_LIMIT = "100/minute"
