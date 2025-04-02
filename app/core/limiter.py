from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["2000 per day", "100 per hour"],
    headers_enabled=True,
)
