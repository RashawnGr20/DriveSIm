import os

from slowapi import Limiter
from slowapi.util import get_remote_address

_TRUST_PROXY = os.getenv("TRUST_PROXY_HEADER", "").strip().lower() in ("1", "true", "yes")


def _client_key(request):
    if _TRUST_PROXY:
        cf = request.headers.get("cf-connecting-ip")
        if cf:
            return cf
        xff = request.headers.get("x-forwarded-for")
        if xff:
            return xff.split(",")[0].strip()
    return get_remote_address(request)


limiter = Limiter(key_func=_client_key)
